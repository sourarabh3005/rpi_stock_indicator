from RPLCD.i2c import CharLCD
from time import sleep


lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=20,
    rows=4,
    charmap='A00',
    auto_linebreaks=False
)


# -------------------------------------------------
# Inverted characters
#
# Dark pixels = background
# Light pixels = actual letter
#
# Each character is 5x8 pixels.
# -------------------------------------------------

inverted_chars = {

    'H': [
        0b00000,
        0b01110,
        0b01110,
        0b01110,
        0b00000,
        0b01110,
        0b01110,
        0b00000,
    ],

    'E': [
        0b00000,
        0b01111,
        0b01111,
        0b00001,
        0b01111,
        0b01111,
        0b01111,
        0b00000,
    ],

    'L': [
        0b00000,
        0b01111,
        0b01111,
        0b01111,
        0b01111,
        0b01111,
        0b01111,
        0b00000,
    ],

    'O': [
        0b00000,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b00000,
    ],

    'W': [
        0b00000,
        0b01110,
        0b01110,
        0b01010,
        0b01010,
        0b01010,
        0b00100,
        0b00000,
    ],

    'R': [
        0b00000,
        0b01110,
        0b01110,
        0b00001,
        0b01011,
        0b01101,
        0b01110,
        0b00000,
    ],

    'D': [
        0b00000,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b00000,
    ],
}


try:

    lcd.clear()
    lcd.backlight_enabled = True

    # -------------------------------------------------
    # Create all custom characters
    # -------------------------------------------------

    char_map = {}

    for index, (character, pattern) in enumerate(
        inverted_chars.items()
    ):

        lcd.create_char(index, pattern)

        char_map[character] = index


    # -------------------------------------------------
    # Line 1 - Normal HELLO WORLD
    # -------------------------------------------------

    lcd.cursor_pos = (0, 0)

    lcd.write_string("HELLO WORLD")


    # -------------------------------------------------
    # Line 2 - Inverted HELLO WORLD
    # -------------------------------------------------

    lcd.cursor_pos = (1, 0)

    for character in "HELLO WORLD":

        if character == ' ':

            lcd.write_string(" ")

        else:

            lcd.write(
                bytes([char_map[character]])
            )


    # Keep displayed
    sleep(60)


finally:

    lcd.clear()
    lcd.close()