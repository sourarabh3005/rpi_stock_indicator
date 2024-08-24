import RPi.GPIO as GPIO
import time
from enum import Enum

from collections import namedtuple

# Define a structure with a value and a flag
TaskItem = namedtuple('TaskItem', ['value', 'flag'])

class GpioPin(Enum):
    #            GPIO_n, IsOutput
    SYS_R = TaskItem(21, True)
    SYS_G = TaskItem(16, True)
    SYS_B = TaskItem(20, True)
    STK_G = TaskItem(23, True)
    STK_Y = TaskItem(22, True)
    STK_R = TaskItem(27, True)
    SW    = TaskItem(26, False)

class SystemState(Enum):
    DEFAULT = 1          # R=1 G=1 B=0 :: Blue
    RUNNING = 2          # R=1 G=0 B=1 :: Green
    INTERNET_DOWN = 3    # R=0 G=1 B=0 :: Magenta
    SYSTEM_ERROR = 4     # R=0 G=1 B=1 :: Red
    AP_MODE = 5          # R=0 G=0 B=0 :: White


def startup_blink():
  # Turn all LED's ON
  GPIO.output(GpioPin.SYS_R.value.value, GPIO.LOW)
  GPIO.output(GpioPin.SYS_G.value.value, GPIO.LOW)
  GPIO.output(GpioPin.SYS_B.value.value, GPIO.LOW)
  GPIO.output(GpioPin.STK_G.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.STK_Y.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.STK_R.value.value, GPIO.HIGH)
  
  time.sleep(1)
  
  # Turn all LED's OFF
  GPIO.output(GpioPin.SYS_R.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.SYS_G.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.SYS_B.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.STK_G.value.value, GPIO.LOW)
  GPIO.output(GpioPin.STK_Y.value.value, GPIO.LOW)
  GPIO.output(GpioPin.STK_R.value.value, GPIO.LOW)  

def system_led_transition(state: SystemState):
  GPIO.output(GpioPin.SYS_R.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.SYS_G.value.value, GPIO.HIGH)
  GPIO.output(GpioPin.SYS_B.value.value, GPIO.HIGH)
  
  if state == SystemState.DEFAULT:
    print("Transition to DEFAULT: Set LED to Blue")
    GPIO.output(GpioPin.SYS_B.value.value, GPIO.LOW)
  elif state == SystemState.RUNNING:
    print("Running")
    GPIO.output(GpioPin.SYS_G.value.value, GPIO.LOW)
  elif state == SystemState.INTERNET_DOWN:
    print("Transition to INTERNET_DOWN: Set LED to Magenta")
    GPIO.output(GpioPin.SYS_R.value.value, GPIO.LOW)
    GPIO.output(GpioPin.SYS_B.value.value, GPIO.LOW)
  elif state == SystemState.SYSTEM_ERROR:
    print("Transition to SYSTEM_ERROR: Set LED to Red")
    GPIO.output(GpioPin.SYS_R.value.value, GPIO.LOW)
  elif state == SystemState.AP_MODE:
    print("AP Mode")
    GPIO.output(GpioPin.SYS_R.value.value, GPIO.LOW)
    GPIO.output(GpioPin.SYS_G.value.value, GPIO.LOW)
    GPIO.output(GpioPin.SYS_B.value.value, GPIO.LOW)
  else:
    print("Default")
    
  
def configure_gpio():
  # Pin Setup
  GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

  for task in GpioPin:
    print(f"Task: {task.name}, Value: {task.value.value}, Flag: {task.value.flag}")  
    if task.value.flag is True:
      GPIO.setup(task.value.value, GPIO.OUT)  # Set led pin as output (optional)      
    else:
      GPIO.setup(task.value.value, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set led pin as output (optional)
      
  startup_blink()
  time.sleep(1)
  system_led_transition(SystemState.DEFAULT)
  
def set_stk_led(buy, sell, crt, set):
  if buy:
    GPIO.output(GpioPin.STK_Y.value.value, set)
    
  if sell:
    GPIO.output(GpioPin.STK_G.value.value, set)
    
  if crt:
    GPIO.output(GpioPin.STK_R.value.value, set)
  
  


