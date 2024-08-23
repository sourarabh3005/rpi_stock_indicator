import threading
import time

class GpioThread(threading.Thread):
    def __init__(self, to_gpio_queue, to_system_queue):
        super().__init__()
        self.to_gpio_queue = to_gpio_queue
        self.to_system_queue = to_system_queue
        self.stop_event = threading.Event()

    def handle_task(self, task, message):
        print(f"GpioThread is handling task: {task} with message: {message}")
        # Simulate task processing
        time.sleep(2)
        return 0  # Return 0 on success

    def run(self):
        while not self.stop_event.is_set():
            # Simulate doing its own job
            print("GpioThread is doing its own job...")
            time.sleep(1)

            # Wait for incoming tasks from System, without throwing an exception if the queue is empty
            task, message = self.to_gpio_queue.get(block=True, timeout=None)  # Blocking wait
            if task is not None:
                print(f"GpioThread received task: {task} with message: {message}")
                ret_code = self.handle_task(task, message)
                if ret_code != 0:
                    self.to_system_queue.put((task, "Error occurred in task"))
                else:
                    self.to_system_queue.put((task, "Task completed successfully"))
            self.to_gpio_queue.task_done()

    def stop(self):
        print("Stopping GpioThread...")
        self.stop_event.set()