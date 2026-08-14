import RPi.GPIO as GPIO
import time

SW = 26
LED = 23

GPIO.setmode(GPIO.BCM)

# Switch connected between GPIO26 and GND
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


def switch_event(channel):
    if GPIO.input(SW) == GPIO.LOW:
        # Switch pressed
        print("Switch PRESSED - LED ON")
        GPIO.output(LED, GPIO.HIGH)
    else:
        # Switch released
        print("Switch RELEASED - LED OFF")
        GPIO.output(LED, GPIO.LOW)


try:
    GPIO.add_event_detect(
        SW,
        GPIO.BOTH,
        callback=switch_event,
        bouncetime=200
    )

    print("Waiting for switch...")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()