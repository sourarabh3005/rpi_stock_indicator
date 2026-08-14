from RPLCD.i2c import CharLCD
from time import sleep

# Change address if i2cdetect shows something else
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=20,
    rows=4,
    charmap='A00'
)

# Custom heart character (5x8 pixels)
heart = (
    0b01010,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000,
    0b00000
)

D_dark = (
        0b11111,
        0b00001,
        0b10101,
        0b10101,
        0b10101,
        0b10101,
        0b00001,
        0b11111,
)


lcd.clear()

# Store heart in custom character slot 0
lcd.create_char(0, heart)
lcd.create_char(1, D_dark)

# Print on Line 2 (row index 1)
lcd.cursor_pos = (1, 0)

lcd.write_string("I ")
lcd.write_string(chr(0))  # Display heart
lcd.write_string(" YOU POTOL")

# Print on Line 3 (row index 1)
lcd.cursor_pos = (2, 0)
lcd.write_string(chr(1))  # Display heart

# Keep message displayed
sleep(60)

lcd.clear()