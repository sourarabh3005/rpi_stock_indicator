

import threading
import time
import queue

# Define tasks
TASK_1 = 1
TASK_2 = 2

class StockThread(threading.Thread):
    def __init__(self, to_stock_queue, to_system_queue):
        super().__init__()
        self.to_stock_queue = to_stock_queue
        self.to_system_queue = to_system_queue
        self.stop_event = threading.Event()

    def handle_task(self, task, message):
        print(f"StockThread is handling task: {task} with message: {message}")
        # Simulate task processing
        time.sleep(2)
        return -1  # Return 0 on success

    def run(self):
        while not self.stop_event.is_set():
            # Simulate doing its own job
            print("StockThread is doing its own job...")
            time.sleep(1)

            try:
                # Wait for incoming tasks from System, with a 60-second timeout
                task, message = self.to_stock_queue.get(timeout=60)
                if task is not None:
                    print(f"StockThread received task: {task} with message: {message}")
                    ret_code = self.handle_task(task, message)
                    if ret_code != 0:
                        self.to_system_queue.put((task, "Error occurred in task"))
                    else:
                        self.to_system_queue.put((task, "Task completed successfully"))
                self.to_stock_queue.task_done()
            except queue.Empty:
                # If 60 seconds expire without receiving a task, execute this code
                print("StockThread did not receive any task for 60 seconds. Executing timeout code.")
                self.execute_timeout_code()

    def execute_timeout_code(self):
        # This function will execute if 60 seconds pass without a new task
        print("Executing timeout code in StockThread...")

    def stop(self):
        print("Stopping StockThread...")
        self.stop_event.set()