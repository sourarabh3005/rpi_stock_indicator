import queue
from thread_gpio import GpioThread, TASK_GP_STSTEM_DEFAULT, TASK_GP_SYSTEM_RUNNING, TASK_GP_INTERNET_DOWN

def main():
    # Create queues for IPC
    gp_task_queue = queue.Queue()
    gp_result_queue = queue.Queue()
    
    # Create and start the worker thread
    gp_worker = GpioThread(gp_task_queue, gp_result_queue)
    gp_worker.start()

    try:
        # Enqueue different tasks with messages
        tasks = [
            (TASK_GP_STSTEM_DEFAULT, "Hello from Task 1"),
            (TASK_GP_SYSTEM_RUNNING, "Hello from Task 2"),
            (TASK_GP_INTERNET_DOWN, "Hello from Task 3")
        ]

        for task in tasks:
            gp_task_queue.put(task)
            result = gp_result_queue.get()  # Wait for the task to complete and get the result
            if result != 0:
                print(f"Error encountered during {task[1]}, breaking out.")
                break

        # Wait for any remaining tasks to be completed
        task_queue.join()

    except Exception as e:
        print(f"Exception in main thread: {e}")
    
    finally:
        # Signal the worker thread to exit
        gp_worker.stop()
        gp_task_queue.put((None, None))

        # Wait for the worker thread to exit
        gp_worker.join()
        print("Main thread exiting.")

if __name__ == "__main__":
    main()