import RPi.GPIO as GPIO
import time

RED = 21
GREEN = 16
BLUE = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)


def all_off():
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)


def red_on():
    all_off()
    GPIO.output(RED, GPIO.HIGH)


def green_on():
    all_off()
    GPIO.output(GREEN, GPIO.HIGH)


def blue_on():
    all_off()
    GPIO.output(BLUE, GPIO.HIGH)


try:
    print("RED ON")
    red_on()
    time.sleep(2)

    print("RED OFF")
    all_off()
    time.sleep(1)

    print("GREEN ON")
    green_on()
    time.sleep(2)

    print("GREEN OFF")
    all_off()
    time.sleep(1)

    print("BLUE ON")
    blue_on()
    time.sleep(2)

    print("BLUE OFF")
    all_off()
    time.sleep(1)

    print("All colors ON")
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(BLUE, GPIO.HIGH)
    time.sleep(2)

    print("All colors OFF")
    all_off()

finally:
    all_off()
    GPIO.cleanup()
    print("GPIO cleanup completed")
