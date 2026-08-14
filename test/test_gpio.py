import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(
    26,
    GPIO.FALLING,
    callback=lambda channel: print("BUTTON PRESSED"),
    bouncetime=200
)

print("GPIO26 edge detection is working")