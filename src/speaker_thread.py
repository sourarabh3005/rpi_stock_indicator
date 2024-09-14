import threading
import time
import queue
import pygame
from task_def import TASK_SOUND_STK_SELL, TASK_SOUND_STK_SELL_CLR
from task_def import TASK_SOUND_STK_CRT, TASK_SOUND_STK_CRT_CLR
from task_def import TASK_SOUND_STK_BUY, TASK_SOUND_STK_BUY_CLR
from task_def import TASK_SOUND_ACK
from task_def import TASK_SOUND_BUSY, TASK_SOUND_BUSY_CLR

SPEAKER_INACTIVE_TIME = 10 * 60  # 10 minutes in seconds
NOTIFY_SOUND_PERIOD = 60 # Any notify sound will recurr every 60 Seconds based on priority (file_busy > crt > sell > buy)

sound_path = "/home/sourabh/rpi_stock_indicator/sounds/"
SOUND_DRIP = "water-drip.mp3"
SOUND_SELL = "stk_sell.mp3"
SOUND_BUY = "stk_buy.mp3"
SOUND_CRT = "stk_crt.mp3"
SOUND_BUSY = "busy.mp3"

class SoundThread(threading.Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.running = True
        self.stk_crt_flag = False
        self.stk_buy_flag = False
        self.stk_sell_flag = False  
        self.file_busy_flag = False
        self.last_activity_time = time.time()
        self.last_notify_time = 0

        # Initialize the pygame mixer for sound playback
        pygame.mixer.init()
        print("**************** SoundThread init done *****************")
        self.play_sound(sound_path + SOUND_DRIP, 1)  # Play bubble sound at volume 1

    def run(self):
      while self.running:
        try:
            # Wait for task with timeout
            task, message = self.task_queue.get(timeout=1)
            
            if task is None:
                # If task is None, handle idle state
                self.handle_idle_state()
            else:
                # Otherwise, process the task
                self.handle_task(task, message)
                self.task_queue.task_done()

        except queue.Empty:
            # No task received, handle idle state
            self.handle_idle_state()
            
    def handle_task(self, task, message):
        print(f"********* task : {task} messsage : {message}")
        if task == TASK_SOUND_BUSY:
            self.file_busy_flag = True
        elif task == TASK_SOUND_BUSY_CLR:
            self.file_busy_flag = False
        elif task == TASK_SOUND_STK_CRT:
            self.stk_crt_flag = True
        elif task == TASK_SOUND_STK_CRT_CLR:
            self.stk_crt_flag = False
        elif task == TASK_SOUND_STK_BUY:
            self.stk_buy_flag = True
        elif task == TASK_SOUND_STK_BUY_CLR:
            self.stk_buy_flag = False
        elif task == TASK_SOUND_STK_SELL:
            self.stk_sell_flag = True
        elif task == TASK_SOUND_STK_SELL_CLR:
            self.stk_sell_flag = False
        elif task == TASK_SOUND_ACK:
            self.clear_highest_priority_flag()
            
        self.last_notify_time = 0 



    def handle_idle_state(self):
        # Reset inactivity timer

        #if self.last_notify_time == 0 and time.time() - self.last_notify_time          
        
        #print("speaker handling idle state")
        if self.file_busy_flag or self.stk_crt_flag or self.stk_sell_flag or self.stk_buy_flag:
          delta_time =  time.time() - self.last_notify_time
          if delta_time > NOTIFY_SOUND_PERIOD:
            delta_time = NOTIFY_SOUND_PERIOD # if first time or any notify event arives
          
          if delta_time < NOTIFY_SOUND_PERIOD:
            return
          else:
            self.last_notify_time = time.time()
            
          if self.file_busy_flag:
            self.play_sound(sound_path + SOUND_BUSY, 3)
          elif self.stk_crt_flag:
            self.play_sound(sound_path + SOUND_CRT, 3)
          elif self.stk_sell_flag:
            self.play_sound(sound_path + SOUND_SELL, 3)
          elif self.stk_buy_flag:
            self.play_sound(sound_path + SOUND_BUY, 3)
            
        if time.time() - self.last_activity_time >= SPEAKER_INACTIVE_TIME:
            self.play_sound(sound_path + SOUND_DRIP, 0.3)  # Play bubble sound at volume 1

        

    def play_sound(self, sound_file, volume):
        print(f"playing {sound_file}")
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.set_volume(volume / 10)  # Scale to 0-1
        pygame.mixer.music.play()
        #print("resetting Inactivity")
        self.last_activity_time = time.time()
        



    def clear_highest_priority_flag(self):
        if self.stk_crt_flag:
            self.stk_crt_flag = False
        elif self.stk_sell_flag:
            self.stk_sell_flag = False
        elif self.stk_buy_flag:
            self.stk_buy_flag = False

    def stop(self):
        self.running = False