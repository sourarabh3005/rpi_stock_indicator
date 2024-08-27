# Import the functions from excel_utils.py
from excel_utils import fetch_data_from_excel, update_excel_data
from gdrive import upload_file_to_gdrive
from enum import Enum
from sheet import SystemFields

# Define an enumeration
class idx(Enum):
    S_NO = 0
    TCKR = 1
    BUY_UNIT = 2

file_path = '/home/sourabh/rpi_stock_indicator/tmp/listed_stocks.xlsx'




if __name__ == "__main__":
  data = fetch_data_from_excel(file_path, sheet_name="System Info")
  #row, col = SystemFields.SYS_EXCEL_STATE.value 
  row, col = SystemFields.SYS_CPU_TEMP.value 
  print(f"Fetched data: {data[row][col]}")
  update_excel_data(file_path, "System Info", 2, 2, 43.5)
    
  #upload_file_to_gdrive(file_path)

  #cell_value = data[2][idx.TCKR.value]
  #if cell_value is not None:  # Check if the cell is not NULL or unfilled
  #  print(cell_value)
  #else:
  #  print("Cell is empty")
