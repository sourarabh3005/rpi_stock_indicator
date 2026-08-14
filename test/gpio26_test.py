import lgpio
import time

GPIO = 26

h = lgpio.gpiochip_open(0)

try:
    print("Claiming GPIO26...")

    lgpio.gpio_claim_input(h, GPIO)

    print("GPIO26 successfully claimed.")
    print("Press/release the switch...")

    while True:
        value = lgpio.gpio_read(h, GPIO)
        print("GPIO26 =", value)
        time.sleep(1)

finally:
    lgpio.gpiochip_close(h)
    print("GPIO cleanup completed")