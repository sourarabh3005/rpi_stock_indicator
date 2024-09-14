import threading
import time
from gpio_pins import configure_gpio
from gpio_pins import set_stk_led
from gpio_pins import GpioPin
from gpio_pins import SystemState, system_led_transition_with_check
from queue import Empty  # Import the Empty exception
import RPi.GPIO as GPIO
import task_def
from task_def import TASK_SYSTEM_REBOOT, TASK_SYSTEM_ACK


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
        configure_gpio()
        GPIO.add_event_detect(self.switch_pin, GPIO.FALLING, callback=self.button_callback, bouncetime=200)
        
    def system_led_transition(self, state: SystemState):
        system_led_transition_with_check(state, self.switch_pressed)
        
    def button_callback(self, channel):
        start_time = time.time()
        
        print("Current system state is {curr_state.value}")
        self.system_led_transition(SystemState.AP_MODE)

        self.switch_pressed = True
        # Wait for the button to be released
        while GPIO.input(self.switch_pin) == GPIO.LOW:
            time.sleep(0.01)  # Small delay to prevent CPU overuse
        self.switch_pressed = False

        press_duration = time.time() - start_time
        self.system_led_transition(SystemState.DEFAULT)

        if press_duration >= 0.5 and press_duration < 5:
            self.job1()  # Call job1 if button is pressed for 0.5 to 5 seconds
        elif press_duration >= 5 and press_duration < 10:
            self.job2()  # Call job2 if button is pressed for 5 to 10 seconds
        elif press_duration >= 10:
            self.job3()  # Call job3 if button is pressed for 10 seconds or more

    def job1(self):
        print("Button pressed for 0.5 to 5 seconds: Executing Job 1")
        self.to_system_queue.put((TASK_SYSTEM_ACK, "button pressed Acknoledging system of some event.. Now upto system"))
        self.system_led_transition(SystemState.OFF)
        time.sleep(1)
        self.system_led_transition(SystemState.DEFAULT)
        

    def job2(self):
        print("Button pressed for 5 to 10 seconds: sending reoot command to system")
        self.system_led_transition(SystemState.OFF)
        time.sleep(0.5)
        self.system_led_transition(SystemState.DEFAULT)
        time.sleep(0.5)
        self.system_led_transition(SystemState.OFF)
        time.sleep(0.5)
        self.system_led_transition(SystemState.DEFAULT)
        time.sleep(0.5)
        self.system_led_transition(SystemState.OFF)
        self.to_system_queue.put((TASK_SYSTEM_REBOOT, "5 second button pressed"))


    def job3(self):
        print("Button pressed for 10 seconds or more: Executing Job 3")
        self.system_led_transition(SystemState.DEFAULT)

    def handle_task(self, task, message):
        print(f"GpioThread is handling task: {task} with message: {message}")
        # Simulate task processing
        time.sleep(2)
        return 0  # Return 0 on success

    def run(self):
      while not self.stop_event.is_set():
        # Simulate doing its own job
        #print("GpioThread is doing its own job...")
        if (self.stk_buy or self.stk_sell or self.stk_crt):
          set_stk_led(self.stk_buy, self.stk_sell, self.stk_crt, True)
          time.sleep(0.5)
          set_stk_led(self.stk_buy, self.stk_sell, self.stk_crt, False)
          time.sleep(0.5)
        else:
          time.sleep(1)

        try:
            # Wait for incoming tasks from System, with a short timeout
            task, message = self.to_gpio_queue.get(block=False, timeout=0.1)
            if task is not None:
                print(f"GpioThread received task: {task} with message: {message}")
                ret_code = self.handle_task(task, message)
                if ret_code != 0:
                    self.to_system_queue.put((task, "Error occurred in task"))
                else:
                    self.to_system_queue.put((task, "Task completed successfully"))
                self.to_gpio_queue.task_done()
        except Empty:
            # If the queue is empty, just continue doing the job
            pass

    def stop(self):
        print("Stopping GpioThread...")
        self.stop_event.set()
