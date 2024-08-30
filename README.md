# rpi_stock_indicator
Raspberry Pi Based Long-Term Capital Gain Indicator


The Raspberry Pi Based Long-Term Capital Gain Indicator is a smart stock market monitoring system designed to continuously track stock prices, providing real-time visual and auditory alerts based on stock conditions. Unlike traditional stock market apps that rely on smartphone notifications, this project integrates hardware components (an RGB LED and a speaker) to deliver instant and unmissable alerts. The system fetches data from an Excel sheet stored on Google Drive and monitors stock prices 24x7 throughout the year.

Setup rclone: Manual process in linux command line. Need some patience
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
