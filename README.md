# rpi_stock_indicator
Raspberry Pi Based Long-Term Capital Gain Indicator


The Raspberry Pi Based Long-Term Capital Gain Indicator is a smart stock market monitoring system designed to continuously track stock prices, providing real-time visual and auditory alerts based on stock conditions. Unlike traditional stock market apps that rely on smartphone notifications, this project integrates hardware components (an RGB LED and a speaker) to deliver instant and unmissable alerts. The system fetches data from an Excel sheet stored on Google Drive and monitors stock prices 24x7 throughout the year.

Setup rclone: Manual process in linux command line. Need some patience. Refer rclone guide.
https://www.youtube.com/watch?v=nrzOdwVb5p4
sudo cp -r ~/.config/rclone /root/.config

Additional Python Libraries:
Excel:
pip install openpyxl
Sound:
sudo apt-get install mpg321
pip install gtts pydub 

Inside /etc/rc.local:

echo "Starting system.py" >> /tmp/rc.local.log
export PYTHONPATH=/home/sourabh/.local/lib/python3.9/site-packages:$PYTHONPATH
/usr/bin/python3 /home/sourabh/rpi_stock_indicator/src/system.py >> /tmp/system.log 2>&1 &
echo "finishing system.py" >> /tmp/rc.local.log

Excel cheetsheet:
Insert Date: Ctrl + ;

# First-Time Initialization

This section describes how to initialize the Raspberry Pi Stock Indicator on a fresh Raspberry Pi OS installation.

The project is designed to run continuously on a Raspberry Pi and uses:

* Python 3
* Python virtual environment (`venv`)
* `yfinance` for stock price data
* Google Drive / Excel for the stock configuration
* Raspberry Pi GPIO for RGB LED control
* I2C LCD display
* Speaker for audio notifications
* `systemd` for automatic startup

## 1. Clone the Repository

Clone the repository into the home directory:

```bash
cd ~
git clone https://github.com/sourarabh3005/rpi_stock_indicator.git
cd rpi_stock_indicator
```

## 2. Install Raspberry Pi OS Dependencies

Update the package database:

```bash
sudo apt update
sudo apt upgrade
```

Install Python and virtual-environment support:

```bash
sudo apt install python3-full python3-venv
```

Install the system packages required for audio playback:

```bash
sudo apt install mpg321
```

Make sure I2C is enabled on the Raspberry Pi:

```bash
sudo raspi-config
```

Go to:

```text
Interface Options
    → I2C
        → Enable
```

Reboot if required:

```bash
sudo reboot
```

## 3. Create the Python Virtual Environment

The current Raspberry Pi OS uses an externally managed system Python environment. Therefore, Python packages should be installed inside a virtual environment instead of installing them globally with `pip`.

From the project directory:

```bash
cd ~/rpi_stock_indicator
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

The shell prompt should now contain:

```text
(.venv)
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the Python dependencies:

```bash
python -m pip install openpyxl
python -m pip install RPi.GPIO
python -m pip install yfinance
python -m pip install pygame
python -m pip install gtts
python -m pip install pydub
python -m pip install RPLCD
```

Verify the important modules:

```bash
python -c "import openpyxl, RPi.GPIO, yfinance, pygame, gtts, pydub, RPLCD; print('Python dependencies OK')"
```

> **Note:** If additional Python dependencies are introduced into the project in the future, update this section or add a `requirements.txt` file.

## 4. Google Drive / Excel Configuration

The project uses an Excel spreadsheet stored on Google Drive as the stock database.

`rclone` is used to access the Google Drive storage.

Install `rclone`:

```bash
sudo apt install rclone
```

Configure the Google Drive remote:

```bash
rclone config
```

Create/configure a Google Drive remote according to the rclone configuration instructions.

Verify that the remote is accessible:

```bash
rclone listremotes
```

Test access to Google Drive:

```bash
rclone lsd <remote-name>:
```

Replace `<remote-name>` with the name configured during `rclone config`.

### rclone configuration for the application

The application may run as a `systemd` service under the Raspberry Pi user account. Make sure the rclone configuration is available to that user.

Check the configuration:

```bash
ls -la ~/.config/rclone/
```

If the application needs to run under another user, make sure that user's rclone configuration is available as well.

## 5. Excel Stock Database

The Excel file contains the stock information monitored by the application.

Make sure the required Excel file is available in the configured Google Drive location.

The application uses `openpyxl` to read and update the workbook.

The Excel sheet should contain the columns expected by the code in:

```text
src/stocks.py
src/excel_utils.py
```

When adding or modifying dates in Excel, the following shortcut can be used:

```text
Ctrl + ;
```

to insert the current date in Excel.

## 6. Hardware Connections

Connect the following hardware to the Raspberry Pi:

### RGB LED

The RGB LED is used to indicate the current stock condition.

The GPIO pin assignments are defined in:

```text
src/gpio_pins.py
```

Always verify the GPIO assignments in that file before connecting the hardware.

### Speaker

The speaker is used for audio notifications.

The project uses `pygame` and/or the configured audio playback utilities to generate notifications.

Verify that the Raspberry Pi can output audio before running the complete application.

### I2C LCD

The project uses an I2C LCD display.

Verify that I2C is enabled:

```bash
sudo raspi-config
```

Then check whether the LCD is detected:

```bash
sudo apt install i2c-tools
i2cdetect -y 1
```

The LCD should normally appear at the configured I2C address.

For example:

```text
0x27
```

The I2C address used by the application should match the address defined in the source code.

## 7. Test the Application Manually

Before configuring automatic startup, always test the application manually.

Activate the virtual environment:

```bash
cd ~/rpi_stock_indicator
source .venv/bin/activate
```

Run:

```bash
python src/system.py
```

Check the following:

1. Python application starts without import errors.
2. Google Drive / Excel data can be accessed.
3. Stock prices can be retrieved.
4. LCD operates correctly.
5. RGB LED changes according to the stock state.
6. Speaker produces the expected notification.
7. No unexpected exceptions appear in the terminal.

Stop the application with:

```text
Ctrl + C
```

Do not configure `systemd` until the application works correctly when started manually.

## 8. Configure Automatic Startup Using systemd

Create a systemd service:

```bash
sudo nano /etc/systemd/system/rpi-stock-indicator.service
```

Add:

```ini
[Unit]
Description=Raspberry Pi Stock Indicator
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=dash
WorkingDirectory=/home/dash/rpi_stock_indicator
ExecStart=/home/dash/rpi_stock_indicator/.venv/bin/python /home/dash/rpi_stock_indicator/src/system.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

> Replace `dash` with the actual Raspberry Pi username if different.

Save the file and reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service so that it starts automatically after boot:

```bash
sudo systemctl enable rpi-stock-indicator.service
```

Start it:

```bash
sudo systemctl start rpi-stock-indicator.service
```

Check the status:

```bash
sudo systemctl status rpi-stock-indicator.service
```

## 9. View Application Logs

To view the application logs:

```bash
journalctl -u rpi-stock-indicator.service
```

To follow the logs in real time:

```bash
journalctl -u rpi-stock-indicator.service -f
```

To view logs from the current boot:

```bash
journalctl -u rpi-stock-indicator.service -b
```

## 10. Restart / Stop the Application

Restart:

```bash
sudo systemctl restart rpi-stock-indicator.service
```

Stop:

```bash
sudo systemctl stop rpi-stock-indicator.service
```

Start:

```bash
sudo systemctl start rpi-stock-indicator.service
```

Disable automatic startup:

```bash
sudo systemctl disable rpi-stock-indicator.service
```

## 11. Verify Automatic Startup

After everything is configured, reboot the Raspberry Pi:

```bash
sudo reboot
```

After reconnecting, check:

```bash
sudo systemctl status rpi-stock-indicator.service
```

The service should show:

```text
Active: active (running)
```

The application should now start automatically after every Raspberry Pi boot.

## Initialization Checklist

Use this checklist when setting up a new Raspberry Pi:

* [ ] Raspberry Pi OS installed
* [ ] I2C enabled
* [ ] Repository cloned
* [ ] Python virtual environment created
* [ ] Python dependencies installed
* [ ] `rclone` installed
* [ ] Google Drive configured
* [ ] Excel database configured
* [ ] RGB LED connected
* [ ] Speaker connected
* [ ] I2C LCD connected
* [ ] LCD detected using `i2cdetect`
* [ ] Application tested manually
* [ ] `systemd` service created
* [ ] Service enabled
* [ ] Service starts successfully
* [ ] Application verified after reboot

