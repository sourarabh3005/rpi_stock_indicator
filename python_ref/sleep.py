import time
import os

def simulate_sleep(sleep_duration):
    # Reduce power consumption by turning off display
    os.system("vcgencmd display_power 0")  # Turn off HDMI

    # Sleep for the specified duration (simulating a low-power mode)
    time.sleep(sleep_duration)

    # Resume by turning the display back on
    os.system("vcgencmd display_power 1")  # Turn on HDMI

# Simulate sleep for 10 seconds
simulate_sleep(10)