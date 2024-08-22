import RPi.GPIO as GPIO
import time

system_green = 16

def configure_gpio():
  # Pin Setup
  GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
  #GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set switch pin as input with pull-up
  GPIO.setup(system_green, GPIO.OUT)  # Set led pin as output (optional)
  
def system_led_on(pin):
  GPIO.output(pin, GPIO.LOW)
  
def system_led_off(pin):
  GPIO.output(pin, GPIO.HIGH)