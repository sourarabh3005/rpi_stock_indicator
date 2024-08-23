import RPi.GPIO as GPIO
import time

# Pin Definitions
switch_pin = 17  # GPIO pin connected to the switch
led_pin = 27     # GPIO pin connected to the LED (for visual feedback)

# Pin Setup
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set switch pin as input with pull-up
GPIO.setup(led_pin, GPIO.OUT)  # Set led pin as output (optional)

# Function to handle the interrupt
def button_callback(channel):
    start_time = time.time()
    
    # Wait for the button to be released
    while GPIO.input(switch_pin) == GPIO.LOW:
        time.sleep(0.01)  # Small delay to prevent CPU overuse
    
    press_duration = time.time() - start_time
    
    if press_duration >= 0.5 and press_duration < 5:
        job1()  # Call job1 if button is pressed for 0.5 to 5 seconds
    elif press_duration >= 5 and press_duration < 10:
        job2()  # Call job2 if button is pressed for 5 to 10 seconds
    elif press_duration >= 10:
        job3()  # Call job3 if button is pressed for 10 seconds or more

def job1():
    print("Button pressed for 0.5 to 5 seconds: Executing Job 1")
    GPIO.output(led_pin, GPIO.HIGH)  # Turn on the LED (optional feedback)
    time.sleep(1)
    GPIO.output(led_pin, GPIO.LOW)   # Turn off the LED

def job2():
    print("Button pressed for 5 to 10 seconds: Executing Job 2")
    GPIO.output(led_pin, GPIO.HIGH)  # Turn on the LED (optional feedback)
    time.sleep(2)
    GPIO.output(led_pin, GPIO.LOW)   # Turn off the LED

def job3():
    print("Button pressed for 10 seconds or more: Executing Job 3")
    GPIO.output(led_pin, GPIO.HIGH)  # Turn on the LED (optional feedback)
    time.sleep(3)
    GPIO.output(led_pin, GPIO.LOW)   # Turn off the LED

# Set up an interrupt on the falling edge of the button press
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    print("Waiting for button press...")
    while True:
        time.sleep(1)  # Keep the program running

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Clean up GPIO settings before exiting