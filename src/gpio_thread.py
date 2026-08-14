import threading
import time

from gpio_pins import configure_gpio
from gpio_pins import set_stk_led
from gpio_pins import GpioPin
from gpio_pins import SystemState, system_led_transition_with_check

from queue import Empty

import RPi.GPIO as GPIO

from task_def import (
    TASK_SYSTEM_BUSY,
    TASK_SYSTEM_ACK,
    TASK_SYSTEM_DEFAULT,
    TASK_SYSTEM_RUNNING,
    TASK_SYSTEM_STK_BUY,
    TASK_SYSTEM_STK_BUY_CLR,
    TASK_SYSTEM_STK_SELL,
    TASK_SYSTEM_STK_SELL_CLR,
    TASK_SYSTEM_STK_CRT,
    TASK_SYSTEM_STK_CRT_CLR,
)

# Switch polling interval
SWITCH_POLL_INTERVAL = 0.1   # 100 ms


class GpioThread(threading.Thread):

    stk_sell = False
    stk_buy = False
    stk_crt = False

    switch_pin = GpioPin.SW.value.value
    switch_pressed = False

    def __init__(self, to_gpio_queue, to_system_queue):

        super().__init__()

        self.to_gpio_queue = to_gpio_queue
        self.to_system_queue = to_system_queue

        self.stop_event = threading.Event()

        # Configure GPIO pins
        configure_gpio()

        print(
            f"GPIO initialized. "
            f"Switch GPIO = {self.switch_pin}"
        )

    # ---------------------------------------------------------
    # System LED
    # ---------------------------------------------------------

    def system_led_transition(self, state: SystemState):

        system_led_transition_with_check(
            state,
            self.switch_pressed
        )

    # ---------------------------------------------------------
    # Switch polling
    # ---------------------------------------------------------

    def poll_switch(self):

        switch_state = GPIO.input(self.switch_pin)

        # -----------------------------------------------------
        # Switch PRESSED
        # -----------------------------------------------------

        if switch_state == GPIO.LOW and not self.switch_pressed:

            self.switch_pressed = True

            self.press_start_time = time.time()

            print("Switch PRESSED")

            self.system_led_transition(
                SystemState.AP_MODE
            )

        # -----------------------------------------------------
        # Switch RELEASED
        # -----------------------------------------------------

        elif switch_state == GPIO.HIGH and self.switch_pressed:

            self.switch_pressed = False

            press_duration = (
                time.time() - self.press_start_time
            )

            print(
                f"Switch RELEASED "
                f"(pressed for {press_duration:.2f} seconds)"
            )

            self.system_led_transition(
                SystemState.DEFAULT
            )

            # -------------------------------------------------
            # Execute appropriate button job
            # -------------------------------------------------

            if 0.5 <= press_duration < 3:

                self.job1()

            elif 3 <= press_duration < 10:

                self.job2()

            elif press_duration >= 10:

                self.job3()

    # ---------------------------------------------------------
    # Button Job 1
    # ---------------------------------------------------------

    def job1(self):

        print(
            "Button pressed for 0.5 to 3 seconds: "
            "Executing Job 1"
        )

        self.to_system_queue.put(
            (
                TASK_SYSTEM_ACK,
                "Button pressed - acknowledging system"
            )
        )

        self.system_led_transition(
            SystemState.OFF
        )

        time.sleep(1)

        self.system_led_transition(
            SystemState.DEFAULT
        )

    # ---------------------------------------------------------
    # Button Job 2
    # ---------------------------------------------------------

    def job2(self):

        print(
            "Button pressed for 3 to 10 seconds: "
            "sending busy command to system"
        )

        self.system_led_transition(
            SystemState.OFF
        )

        time.sleep(0.5)

        self.system_led_transition(
            SystemState.DEFAULT
        )

        time.sleep(0.5)

        self.system_led_transition(
            SystemState.OFF
        )

        time.sleep(0.5)

        self.system_led_transition(
            SystemState.DEFAULT
        )

        time.sleep(0.5)

        self.system_led_transition(
            SystemState.OFF
        )

        self.to_system_queue.put(
            (
                TASK_SYSTEM_BUSY,
                "3 second button pressed"
            )
        )

    # ---------------------------------------------------------
    # Button Job 3
    # ---------------------------------------------------------

    def job3(self):

        print(
            "Button pressed for 10 seconds or more: "
            "Executing Job 3"
        )

        self.system_led_transition(
            SystemState.DEFAULT
        )

    # ---------------------------------------------------------
    # Handle messages from System thread
    # ---------------------------------------------------------

    def handle_task(self, task, message):

        print(
            f"GpioThread is handling task: "
            f"{task} with message: {message}"
        )

        # -----------------------------------------------------
        # System state
        # -----------------------------------------------------

        if task == TASK_SYSTEM_DEFAULT:

            print("GPIO: System state DEFAULT")

            self.system_led_transition(
                SystemState.DEFAULT
            )

        elif task == TASK_SYSTEM_RUNNING:

            print("GPIO: System state RUNNING")

            self.system_led_transition(
                SystemState.RUNNING
            )

        # -----------------------------------------------------
        # Stock BUY
        # -----------------------------------------------------

        elif task == TASK_SYSTEM_STK_BUY:

            print("GPIO: Stock BUY detected")

            self.stk_buy = True

        elif task == TASK_SYSTEM_STK_BUY_CLR:

            print("GPIO: Stock BUY cleared")

            self.stk_buy = False

        # -----------------------------------------------------
        # Stock SELL
        # -----------------------------------------------------

        elif task == TASK_SYSTEM_STK_SELL:

            print("GPIO: Stock SELL detected")

            self.stk_sell = True

        elif task == TASK_SYSTEM_STK_SELL_CLR:

            print("GPIO: Stock SELL cleared")

            self.stk_sell = False

        # -----------------------------------------------------
        # Stock CRITICAL
        # -----------------------------------------------------

        elif task == TASK_SYSTEM_STK_CRT:

            print("GPIO: Stock CRITICAL detected")

            self.stk_crt = True

        elif task == TASK_SYSTEM_STK_CRT_CLR:

            print("GPIO: Stock CRITICAL cleared")

            self.stk_crt = False

        # -----------------------------------------------------
        # BUSY
        # -----------------------------------------------------

        elif task == TASK_SYSTEM_BUSY:

            print("GPIO received BUSY task")

        else:

            print(
                f"GPIO received unknown task: {task}"
            )

    # ---------------------------------------------------------
    # Main GPIO thread
    # ---------------------------------------------------------

    def run(self):

        print(
            "GpioThread started. "
            "Switch polling interval = 100 ms"
        )

        try:

            while not self.stop_event.is_set():

                # -------------------------------------------------
                # Poll switch
                # -------------------------------------------------

                self.poll_switch()

                # -------------------------------------------------
                # Process ALL pending System -> GPIO messages
                # -------------------------------------------------

                while True:

                    try:

                        task, message = (
                            self.to_gpio_queue.get(
                                block=False
                            )
                        )

                    except Empty:

                        break

                    try:

                        if task is not None:

                            print(
                                f"GpioThread received task: "
                                f"{task} with message: {message}"
                            )

                            self.handle_task(
                                task,
                                message
                            )

                    finally:

                        self.to_gpio_queue.task_done()

                # -------------------------------------------------
                # Stock LEDs
                # -------------------------------------------------

                if (
                    self.stk_buy
                    or self.stk_sell
                    or self.stk_crt
                ):

                    set_stk_led(
                        self.stk_buy,
                        self.stk_sell,
                        self.stk_crt,
                        True
                    )

                    time.sleep(0.5)

                    set_stk_led(
                        self.stk_buy,
                        self.stk_sell,
                        self.stk_crt,
                        False
                    )

                    time.sleep(0.5)

                else:

                    time.sleep(
                        SWITCH_POLL_INTERVAL
                    )

        finally:

            print(
                "GpioThread cleaning up GPIO..."
            )

            try:

                set_stk_led(
                    False,
                    False,
                    False,
                    False
                )

                system_led_transition_with_check(
                    SystemState.OFF,
                    False
                )

            except Exception as e:

                print(
                    f"Error while turning LEDs off: {e}"
                )

            GPIO.cleanup()

            print(
                "GpioThread GPIO cleanup completed."
            )

    # ---------------------------------------------------------
    # Stop
    # ---------------------------------------------------------

    def stop(self):

        print(
            "Stopping GpioThread..."
        )

        self.stop_event.set()