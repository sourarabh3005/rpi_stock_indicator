import threading
import time
import queue
from gpio_thread import GpioThread  # Import GpioThread from thread.py
from stock_thread import StockThread, TASK_1, TASK_2  # Import StockThread and tasks from thread2.py

class System:
    def __init__(self):
        self.to_gpio_queue = queue.Queue()  # Queue for messages to GpioThread
        self.to_stock_queue = queue.Queue()  # Queue for messages to StockThread
        self.to_system_queue = queue.Queue()  # Queue for messages to System
        self.stop_event = threading.Event()
        self.mutex = threading.Lock()  # Mutex for shared resources

    def message_queue_handler(self):
        while not self.stop_event.is_set():
            try:
                with self.mutex:
                    # Process messages from both GpioThread and StockThread
                    task, message = self.to_system_queue.get(timeout=1)
                    if task is not None:
                        print(f"System received task: {task} with message: {message}")
                    self.to_system_queue.task_done()
            except queue.Empty:
                continue

    def print_message_loop(self):
        while not self.stop_event.is_set():
            with self.mutex:
                print("System is doing its own job...")
            time.sleep(1)

    def start(self):
        self.gpio_thread = GpioThread(self.to_gpio_queue, self.to_system_queue)
        self.gpio_thread.start()

        self.stock_thread = StockThread(self.to_stock_queue, self.to_system_queue)
        self.stock_thread.start()

        threading.Thread(target=self.message_queue_handler, daemon=True).start()

        # Pass TASK_1 and TASK_2 to StockThread
        self.to_stock_queue.put((TASK_1, "Message for TASK_1"))
        self.to_stock_queue.put((TASK_2, "Message for TASK_2"))

        try:
            self.print_message_loop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("Stopping system...")
        self.stop_event.set()
        self.gpio_thread.stop()
        self.stock_thread.stop()
        self.gpio_thread.join()
        self.stock_thread.join()

def main():
    system = System()
    system.start()

if __name__ == "__main__":
    main()
