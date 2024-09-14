

import threading
import time
import queue
from stocks import monitor_stock_market

STOCK_THREAD_DELAY = 80


class StockThread(threading.Thread):
    cpu_temp = 0
    num_sell_stk = 0
    num_buy_stk = 0
    num_crt_stk = 0
    last_monitor_time = 0
    
    def __init__(self, to_stock_queue, to_system_queue):
        super().__init__()
        self.to_stock_queue = to_stock_queue
        self.to_system_queue = to_system_queue
        self.stop_event = threading.Event()
        time.sleep(1)

    def handle_task(self, task, message):
        print(f"StockThread is handling task: {task} with message: {message}")
        time.sleep(1)
        return 0  # Return 0 on success

    def run(self):
        while not self.stop_event.is_set():
            # Simulate doing its own job
            print("StockThread is doing its own job...")
            time.sleep(1)

            try:
                # Wait for incoming tasks from System, with a 60-second timeout
                stock_queue_timeout =  time.time() - self.last_monitor_time
                print(f"stock_thread : {self.last_monitor_time} timeout was computed to {stock_queue_timeout}")
                
                if stock_queue_timeout >= STOCK_THREAD_DELAY:
                  stock_queue_timeout = 5
                
                self.last_monitor_time = time.time() 
                print(f"stock_thread is waiting for message till {stock_queue_timeout} seconds")
                
                task, message = self.to_stock_queue.get(timeout=stock_queue_timeout)
                
                
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
                print("StockThread did not receive any task. Executing timeout code.")
                self.execute_timeout_code()

    def execute_timeout_code(self):
        # This function will execute if 60 seconds pass without a new task
        print(f"Executing timeout code in StockThread... cpu_temp {self.cpu_temp}")
        monitor_stock_market(self)

    def stop(self):
        print("Stopping StockThread...")
        self.stop_event.set()
