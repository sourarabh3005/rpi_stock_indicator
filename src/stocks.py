# Import the functions from excel_utils.py
from excel_utils import fetch_data_from_excel, update_excel_data, change_cell_color
from gdrive import upload_file_to_gdrive, download_file_from_gdrive
from enum import Enum
from sheet import SystemFields
import shutil
from openpyxl import load_workbook
from datetime import datetime

def copy_file(src, dest):
    """
    Copy a file from src to dest.

    :param src: Source file path
    :param dest: Destination file path
    """
    try:
        shutil.copy(src, dest)
        print(f"File copied successfully from {src} to {dest}.")
    except FileNotFoundError:
        print(f"Source file not found: {src}")
    except PermissionError:
        print(f"Permission denied. Cannot copy file to {dest}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def get_current_date():
    """
    Returns the current date in the format YYYY-MM-DD.
    """
    current_date = datetime.now().date()
    return current_date.strftime("%Y-%m-%d")

def get_current_time():
    """
    Returns the current time in the format HH:MM:SS.
    """
    current_time = datetime.now().time()
    return current_time.strftime("%H:%M:%S")
    
# Define an enumeration
class idx(Enum):
    S_NO = 0
    TCKR = 1
    BUY_UNIT = 2

dload_path = '/home/sourabh/rpi_stock_indicator/tmp/dload'
dload_sysfile_name = '/home/sourabh/rpi_stock_indicator/tmp/dload/system_info.xlsx'
dload_stkfile_name = '/home/sourabh/rpi_stock_indicator/tmp/dload/stock_info.xlsx'
tmp_stkfile_name = '/home/sourabh/rpi_stock_indicator/tmp/stock_info.xlsx'

def file_is_under_edit(file_path):
    data = fetch_data_from_excel(file_path, sheet_name="System Info")
    row, col = SystemFields.SYS_EXCEL_STATE.value 
    print(f"System State: {data[row][col]}")
    if data[row][col] == "Running":
        return False
    else:
        return True

num_sell_stk = 1
num_buy_stk = 1
num_crt_stk = 0
cpu_temp = 40.5

def update_all_system_info(file_path):

    print("Updating all necessary system info")
    data = load_workbook(file_path)
    
    # Sell Status
    if num_sell_stk > 0:
        color = "00FF00"
    else:
        color = "808080"
    r, c = SystemFields.SYS_SELL_STK_FLAG.value
    change_cell_color(data, sheet_name="System Info", row = r, column = c, color=color)
    r, c = SystemFields.SYS_SELL_STK_VAL.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=num_sell_stk)
    
    # Buy Status
    if num_buy_stk > 0:
        color = "FFFF00"
    else:
        color = "808080"
    r, c = SystemFields.SYS_BUY_STK_FLAG.value
    change_cell_color(data, sheet_name="System Info", row = r, column = c, color=color)
    r, c = SystemFields.SYS_BUY_STK_VAL.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=num_buy_stk)
    data.save(file_path)

    # Crt Status
    if num_crt_stk > 0:
        color = "FF0000"
    else:
        color = "808080"
    r, c = SystemFields.SYS_CRT_STK_FLAG.value
    change_cell_color(data, sheet_name="System Info", row = r, column = c, color=color)
    r, c = SystemFields.SYS_CRT_STK_VAL.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=num_crt_stk)

    # CPU Temp
    r, c = SystemFields.SYS_CPU_TEMP.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=cpu_temp)

    # CURRENT DATE
    r, c = SystemFields.SYS_CURR_DATE.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=get_current_date())

    # CURRENT TIME
    r, c = SystemFields.SYS_CURR_TIME.value
    update_excel_data(data, sheet_name="System Info", row = r, column = c, new_value=get_current_time())

    data.save(file_path)    
    
    
    

def monitor_stock_market():
    download_file_from_gdrive(dload_path)
    if file_is_under_edit(dload_sysfile_name) is True:
        print("File under edit")
        return
        

    copy_file(dload_stkfile_name, tmp_stkfile_name)
    
    #process_wishlist(tmp_file_path)
    #download_file_from_gdrive(dload_file_path)

    download_file_from_gdrive(dload_path)
    if file_is_under_edit(dload_sysfile_name) is True:
        print("File under edit")
        return
    update_all_system_info(dload_sysfile_name)
    upload_file_to_gdrive(dload_sysfile_name)
    #upload_file_to_gdrive(tmp_stkfile_name)



if __name__ == "__main__":
    monitor_stock_market()
  #data = fetch_data_from_excel(file_path, sheet_name="System Info")
  #row, col = SystemFields.SYS_EXCEL_STATE.value 
  #row, col = SystemFields.SYS_CPU_TEMP.value 
  #print(f"Fetched data: {data[row][col]}")
  #update_excel_data(file_path, "System Info", 2, 2, 43.5)
    
  #upload_file_to_gdrive(file_path)

  #cell_value = data[2][idx.TCKR.value]
  #if cell_value is not None:  # Check if the cell is not NULL or unfilled
  #  print(cell_value)
  #else:
  #  print("Cell is empty")
