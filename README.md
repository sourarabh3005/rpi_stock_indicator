# rpi_stock_indicator
Raspberry Pi Based Long-Term Capital Gain Indicator


The Raspberry Pi Based Long-Term Capital Gain Indicator is a smart stock market monitoring system designed to continuously track stock prices, providing real-time visual and auditory alerts based on stock conditions. Unlike traditional stock market apps that rely on smartphone notifications, this project integrates hardware components (an RGB LED and a speaker) to deliver instant and unmissable alerts. The system fetches data from an Excel sheet stored on Google Drive and monitors stock prices 24x7 throughout the year.

Setup rclone: Manual process in linux command line. Need some patience
https://www.youtube.com/watch?v=nrzOdwVb5p4

Additional Python Libraries:
Excel:
pip install openpyxl
Sound:
sudo apt-get install mpg321
pip install gtts pydub 

Excel cheetsheet:
Insert Date: Ctrl + ;
