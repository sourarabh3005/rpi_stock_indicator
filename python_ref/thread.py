import threading
import time
import queue

# Define task constants
TASK_1 = 1
TASK_2 = 2
TASK_3 = 3

class WorkerThread(threading.Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.running = True
    
    def run(self):
        while self.running:
            try:
                # Non-blocking queue get with timeout
                task, message = self.task_queue.get(timeout=1)  # Waits for 1 second for a task
                if task is None:  # Check for the stop signal
                    break

                # Handle tasks based on task type
                if task == TASK_1:
                    result = self.handle_task_1(message)
                elif task == TASK_2:
                    result = self.handle_task_2(message)
                elif task == TASK_3:
                    result = self.handle_task_3(message)
                else:
                    result = -1  # Unknown task

                self.result_queue.put(result)
                self.task_queue.task_done()

            except queue.Empty:
                # Queue is empty, do the thread's own job
                self.do_own_job()

    def do_own_job(self):
        print("WorkerThread is doing its own job...")
        time.sleep(0.5)  # Simulate some work
    
    def handle_task_1(self, message):
        print(f"Executing Task 1 with message: {message}")
        time.sleep(0.5)
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
        print("Task 3 completed.")
        # Simulate an error
        return -1  # Error
            
    def stop(self):
        self.running = False
    