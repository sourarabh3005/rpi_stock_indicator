import os
import threading
import time
import queue

from stock_thread import StockThread
from gpio_thread import GpioThread

from wifi_info import get_ipv4_address, get_wifi_ssid

import requests

from task_def import (
    TASK_SYSTEM_BUSY,
    TASK_SYSTEM_DEFAULT,
    TASK_SYSTEM_RUNNING,
    TASK_SYSTEM_ACK
)

from task_def import (
    TASK_SYSTEM_STK_BUY,
    TASK_SYSTEM_STK_SELL,
    TASK_SYSTEM_STK_CRT
)

from task_def import (
    TASK_SYSTEM_STK_BUY_CLR,
    TASK_SYSTEM_STK_SELL_CLR,
    TASK_SYSTEM_STK_CRT_CLR
)


SYSTEM_THREAD_DELAY = 9.5


def get_cpu_temperature():
    """
    Returns the current temperature of the Raspberry Pi CPU
    in degrees Celsius.
    """

    try:
        with open(
            "/sys/class/thermal/thermal_zone0/temp",
            "r"
        ) as f:

            temp = f.read()

        # Temperature is reported in millidegrees.
        return float(temp) / 1000.0

    except FileNotFoundError:

        print(
            "Could not read CPU temperature. "
            "Ensure this is run on a Raspberry Pi."
        )

        return None


def check_internet(
    url='https://www.google.com/',
    timeout=5
):

    try:

        response = requests.get(
            url,
            timeout=timeout
        )

        return response.status_code == 200

    except (
        requests.ConnectionError,
        requests.Timeout
    ):

        return False


def reboot_system():

    try:

        print("Rebooting the system...")
        os.system('sudo reboot')

    except Exception as e:

        print(f"An error occurred: {e}")


class System:

    def __init__(self):

        # ======================================================
        # Queues
        # ======================================================

        self.to_gpio_queue = queue.Queue()
        self.to_stock_queue = queue.Queue()

        self.to_system_queue = queue.Queue()

        # ======================================================
        # Synchronization
        # ======================================================

        self.stop_event = threading.Event()
        self.mutex = threading.Lock()

        # ======================================================
        # Thread handles
        # ======================================================

        self.gpio_thread = None
        self.stock_thread = None

        # Speaker remains disabled for now.
        self.sound_thread = None


    def message_queue_handler(self):

        while not self.stop_event.is_set():

            try:

                with self.mutex:

                    task, message = (
                        self.to_system_queue.get(
                            timeout=1
                        )
                    )

                    if task is not None:

                        print(
                            f"System received task: {task} "
                            f"with message: {message}"
                        )

                        # ==================================================
                        # File busy
                        # ==================================================

                        if task is TASK_SYSTEM_BUSY:

                            if self.stock_thread.file_busy:

                                self.stock_thread.file_busy = False

                                print(
                                    "Clearing the Busy Flag... "
                                    "Wait for stock thread to raise "
                                    "clear busy signal"
                                )

                            else:

                                print(
                                    "Setting File is busy... "
                                    "Wait for stock thread to raise "
                                    "busy signal"
                                )

                                self.stock_thread.file_busy = True


                        # ==================================================
                        # System DEFAULT
                        # ==================================================

                        if task is TASK_SYSTEM_DEFAULT:

                            print(
                                "System state: DEFAULT"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_DEFAULT,
                                    message
                                )
                            )


                        # ==================================================
                        # System RUNNING
                        # ==================================================

                        if task is TASK_SYSTEM_RUNNING:

                            print(
                                "System state: RUNNING"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_RUNNING,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock BUY
                        # ==================================================

                        if task is TASK_SYSTEM_STK_BUY:

                            print(
                                "Stock BUY condition detected"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_BUY,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock BUY cleared
                        # ==================================================

                        if task is TASK_SYSTEM_STK_BUY_CLR:

                            print(
                                "Stock BUY condition cleared"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_BUY_CLR,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock SELL
                        # ==================================================

                        if task is TASK_SYSTEM_STK_SELL:

                            print(
                                "Stock SELL condition detected"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_SELL,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock SELL cleared
                        # ==================================================

                        if task is TASK_SYSTEM_STK_SELL_CLR:

                            print(
                                "Stock SELL condition cleared"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_SELL_CLR,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock Critical
                        # ==================================================

                        if task is TASK_SYSTEM_STK_CRT:

                            print(
                                "Stock CRITICAL condition detected"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_CRT,
                                    message
                                )
                            )


                        # ==================================================
                        # Stock Critical cleared
                        # ==================================================

                        if task is TASK_SYSTEM_STK_CRT_CLR:

                            print(
                                "Stock CRITICAL condition cleared"
                            )

                            self.to_gpio_queue.put(
                                (
                                    TASK_SYSTEM_STK_CRT_CLR,
                                    message
                                )
                            )


                        # ==================================================
                        # ACK
                        # ==================================================

                        if task is TASK_SYSTEM_ACK:

                            print(
                                "Sound acknowledgement received "
                                "(speaker disabled)"
                            )


                    self.to_system_queue.task_done()

            except queue.Empty:

                continue


    def blink_system_led(self):

        """
        System LED handling is performed by GpioThread.
        """

        print(
            "System LED handling delegated to GpioThread"
        )


    def monitor_system(self):

        while not self.stop_event.is_set():

            with self.mutex:

                temp = get_cpu_temperature()

                self.stock_thread.cpu_temp = temp

                print(
                    f"System is doing its own job... "
                    f"CPU temperature: {temp}"
                )

                if check_internet():

                    print("Internet is working.")

                else:

                    print("Internet is not working.")

            time.sleep(SYSTEM_THREAD_DELAY)


    def start(self):

        # ======================================================
        # GPIO ENABLED
        # ======================================================

        print("Starting GPIO thread...")

        self.gpio_thread = GpioThread(
            self.to_gpio_queue,
            self.to_system_queue
        )

        self.gpio_thread.start()

        print("GPIO thread started.")


        # ======================================================
        # SPEAKER DISABLED
        # ======================================================

        # self.to_sound_queue = queue.Queue()

        # self.sound_thread = SoundThread(
        #     self.to_sound_queue,
        #     self.to_system_queue
        # )

        # self.sound_thread.start()


        # ======================================================
        # STOCK MONITORING ENABLED
        # ======================================================

        print("Starting stock monitoring thread...")

        self.stock_thread = StockThread(
            self.to_stock_queue,
            self.to_system_queue
        )

        self.stock_thread.start()

        self.stock_thread.wifi_ssid = (
            get_wifi_ssid()
        )

        self.stock_thread.system_ip = (
            get_ipv4_address()
        )


        # ======================================================
        # System message handler
        # ======================================================

        print(
            "Creating system message handler ..."
        )

        threading.Thread(
            target=self.message_queue_handler,
            daemon=True
        ).start()


        print("----------------------------------------")
        print("System initialization completed")
        print("GPIO    : ENABLED")
        print("Speaker : DISABLED")
        print("Stock   : ENABLED")
        print("----------------------------------------")


        try:

            self.monitor_system()

        except KeyboardInterrupt:

            self.stop()


    def stop(self):

        print("Stopping system...")

        self.stop_event.set()


        # ======================================================
        # Stop GPIO
        # ======================================================

        if self.gpio_thread is not None:

            print("Stopping GPIO thread...")

            self.gpio_thread.stop()


        # ======================================================
        # Stop stock thread
        # ======================================================

        if self.stock_thread is not None:

            print("Stopping stock thread...")

            self.stock_thread.stop()


        # ======================================================
        # Join GPIO
        # ======================================================

        if self.gpio_thread is not None:

            self.gpio_thread.join()


        # ======================================================
        # Join stock
        # ======================================================

        if self.stock_thread is not None:

            self.stock_thread.join()


        print("System stopped.")


def main():

    system = System()

    system.start()


if __name__ == "__main__":

    main()