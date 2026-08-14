import RPi.GPIO as GPIO
import time

SW = 26
LED = 23

POLL_INTERVAL = 0.1  # 100 ms

GPIO.setmode(GPIO.BCM)

# Switch:
# GPIO26 is HIGH when released
# GPIO26 is LOW when pressed (switch connected to GND)
GPIO.setup(
    SW,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP
)

# LED
GPIO.setup(
    LED,
    GPIO.OUT,
    initial=GPIO.LOW
)

try:
    print("GPIO polling test started")
    print("GPIO26 = switch")
    print("GPIO23 = LED")
    print("Polling interval = 100 ms")
    print("Press Ctrl+C to exit")
    print()

    while True:

        switch_state = GPIO.input(SW)

        if switch_state == GPIO.HIGH:
            # Switch released
            GPIO.output(LED, GPIO.HIGH)

        else:
            # Switch pressed
            GPIO.output(LED, GPIO.LOW)

        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleanup completed")
