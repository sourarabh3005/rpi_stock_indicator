import os
import threading
import time
import queue
from gpio_thread import GpioThread  
from stock_thread import StockThread
from gpio_pins import SystemState
from speaker_thread import SoundThread
from wifi_info import get_ipv4_address, get_wifi_ssid
import requests
from task_def import TASK_SYSTEM_BUSY, TASK_SYSTEM_DEFAULT, TASK_SYSTEM_RUNNING, TASK_SYSTEM_ACK
from task_def import TASK_SYSTEM_STK_BUY, TASK_SYSTEM_STK_SELL, TASK_SYSTEM_STK_CRT
from task_def import TASK_SYSTEM_STK_BUY_CLR, TASK_SYSTEM_STK_SELL_CLR, TASK_SYSTEM_STK_CRT_CLR

from task_def import TASK_SOUND_STK_SELL, TASK_SOUND_STK_SELL_CLR
from task_def import TASK_SOUND_STK_CRT, TASK_SOUND_STK_CRT_CLR
from task_def import TASK_SOUND_STK_BUY, TASK_SOUND_STK_BUY_CLR
from task_def import TASK_SOUND_ACK
from task_def import TASK_SOUND_BUSY, TASK_SOUND_BUSY_CLR


SYSTEM_THREAD_DELAY = 9.5

def get_cpu_temperature():
    """
    Returns the current temperature of the Raspberry Pi CPU in degrees Celsius.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
        # The temperature is reported in millidegrees, so we divide by 1000
        return float(temp) / 1000.0
    except FileNotFoundError:
        print("Could not read CPU temperature. Ensure this is run on a Raspberry Pi.")
        return None

def check_internet(url='https://www.google.com/', timeout=5):
    try:
        # Try to make a GET request to the specified URL
        response = requests.get(url, timeout=timeout)
        # If the request is successful, return True
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout):
        # If the request fails due to connection or timeout issues, return False
        return False


def reboot_system():
    try:
        print("Rebooting the system...")
        os.system('sudo reboot')
    except Exception as e:
        print(f"An error occurred: {e}")

class System:
    system_state = SystemState.DEFAULT
    
    def __init__(self):
        self.to_gpio_queue = queue.Queue()  # Queue for messages to GpioThread
        self.to_stock_queue = queue.Queue()  # Queue for messages to StockThread
        self.to_sound_queue = queue.Queue()  # Queue for messages to SoundThread
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
                      
                      if task is TASK_SYSTEM_BUSY:
                        if self.stock_thread.file_busy:
                          self.stock_thread.file_busy = False
                          print("Clearing the Busy Flag... Wait for stock thread to raise clear busy signal")
                        else:
                          print("Setting File is busy... Wait for stock thread to raise busy signal")
                          self.stock_thread.file_busy = True
                        
                      if task is TASK_SYSTEM_DEFAULT:
                        self.system_state = SystemState.DEFAULT
                        self.to_sound_queue.put((TASK_SOUND_BUSY, "File under edit"))
                        
                      if task is TASK_SYSTEM_RUNNING:
                        self.system_state = SystemState.RUNNING
                        self.to_sound_queue.put((TASK_SOUND_BUSY_CLR, "File ready"))
                        
                      if task is TASK_SYSTEM_STK_BUY:
                        self.gpio_thread.stk_buy = True
                        self.to_sound_queue.put((TASK_SOUND_STK_BUY, "Stock Buy set"))
                        
                      if task is TASK_SYSTEM_STK_BUY_CLR:
                        self.gpio_thread.stk_buy = False
                        self.to_sound_queue.put((TASK_SOUND_STK_BUY_CLR, "Stock Buy clear"))

                      if task is TASK_SYSTEM_STK_SELL:
                        self.gpio_thread.stk_sell = True
                        self.to_sound_queue.put((TASK_SOUND_STK_SELL, "Stock Sell set"))
                        
                      if task is TASK_SYSTEM_STK_SELL_CLR:
                        self.gpio_thread.stk_sell = False
                        self.to_sound_queue.put((TASK_SOUND_STK_SELL_CLR, "Stock Sell clear"))
                        
                      if task is TASK_SYSTEM_ACK:
                        self.to_sound_queue.put((TASK_SOUND_ACK, "Acknoledging the sound alert... Now you clear the highest priority alert"))
                        
                    self.to_system_queue.task_done()
            except queue.Empty:
                continue
                
    def blink_system_led(self):
        self.gpio_thread.system_led_transition(self.system_state)
        time.sleep(0.5)
        self.gpio_thread.system_led_transition(SystemState.OFF)
    
    
    ##### WHILE Loop  
    def monitor_system(self):
        while not self.stop_event.is_set():
            with self.mutex:
                temp = get_cpu_temperature()
                self.stock_thread.cpu_temp = temp
                print(f"System is doing its own job...{temp}")
                
                if check_internet():
                  print("Internet is working.")
                  self.blink_system_led()
                else:
                  print("Internet is not working.")
                  self.gpio_thread.system_led_transition(SystemState.INTERNET_DOWN)
                  
            time.sleep(SYSTEM_THREAD_DELAY)

    def start(self):
        self.gpio_thread = GpioThread(self.to_gpio_queue, self.to_system_queue)
        self.gpio_thread.start()

        self.sound_thread = SoundThread(self.to_sound_queue, self.to_system_queue)
        self.sound_thread.start()

        self.stock_thread = StockThread(self.to_stock_queue, self.to_system_queue)
        self.stock_thread.start()
        
        self.stock_thread.wifi_ssid = get_wifi_ssid()
        self.stock_thread.system_ip = get_ipv4_address()
        
        
        print("Creating system message handler ...")
        threading.Thread(target=self.message_queue_handler, daemon=True).start()

        # Pass TASK_1 and TASK_2 to StockThread
        #self.to_stock_queue.put((TASK_1, "Message for TASK_1"))
        #self.to_stock_queue.put((TASK_2, "Message for TASK_2"))
        
        print("All necessary System initialization is done... LED OFF")
        self.gpio_thread.system_led_transition(SystemState.OFF)

        try:
            self.monitor_system()
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
