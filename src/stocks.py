# Import the functions from excel_utils.py
from excel_utils import fetch_data_from_excel, update_excel_data
from gdrive import upload_file_to_gdrive

file_path = '/home/sourabh/proj/rpi_stock_indicator/tmp/listed_stocks.xlsx'

data = fetch_data_from_excel(file_path, sheet_name="Sheet1")
print("Fetched data:")
for row in data:
    print(row)
    
upload_file_to_gdrive(file_path)