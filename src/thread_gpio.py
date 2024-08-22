import threading
import time
import queue
from gpio_led import configure_gpio
from gpio_led import system_led_on
from gpio_led import system_led_off


# Define task constants
TASK_GP_STSTEM_DEFAULT = 1  # System - BLUE # Also if set to reboot 
TASK_GP_SYSTEM_RUNNING = 2  # System - GREEN
TASK_GP_INTERNET_DOWN = 3   # System - RED
TASK_GP_DATABASE_ERROR = 4
TASK_GP_AP_MODE = 5         # System - WHITE
TASK_GP_STOCK_SELL_ON = 6   # Stock - Green Blink 0.5
TASK_GP_STOCK_SELL_OFF = 7  # Stock - Green Blink off
TASK_GP_STOCK_BUY_ON = 8    # Stock - Blue
TASK_GP_STOCK_BUY_OFF = 9
TASK_GP_MARKET_CRITICAL_ON = 10 # Stock Red blink
TASK_GP_MARKET_CRITICAL_OFF = 11



class GpioThread(threading.Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.running = True
        configure_gpio()
    
    def run(self):
        while self.running:
            try:
                # Non-blocking queue get with timeout
                task, message = self.task_queue.get(timeout=1)  # Waits for 1 second for a task
                if task is None:  # Check for the stop signal
                    break

                # Handle tasks based on task type
                if task == TASK_GP_STSTEM_DEFAULT:
                    result = self.handle_task_system_default(message)
                elif task == TASK_GP_SYSTEM_RUNNING:
                    result = self.handle_task_2(message)
                elif task == TASK_GP_INTERNET_DOWN:
                    result = self.handle_task_3(message)
                else:
                    result = -1  # Unknown task

                self.result_queue.put(result)
                self.task_queue.task_done()

            except queue.Empty:
                # Queue is empty, do the thread's own job
                self.do_own_job()

    def do_own_job(self):
        print("Gpio Thread is doing its own job...")
        time.sleep(0.5)  # Simulate some work
    
    def handle_task_system_default(self, message):
        print(f"Executing Task 1 with message: {message}")
        time.sleep(0.5)
        system_led_on(16)
        print("Task 1 completed.")
        return 0  # Success

    def handle_task_2(self, message):
        print(f"Executing Task 2 with message: {message}")
        time.sleep(0.5)
        print("Task 2 completed.")
        return 0  # Success

    def handle_task_3(self, message):
        print(f"Executing Task 3 with message: {message}")
        time.sleep(4)
        system_led_off(16)
        print("Task 3 completed.")
        # Simulate an error
        return -1  # Error
            
    def stop(self):
        self.running = False
    