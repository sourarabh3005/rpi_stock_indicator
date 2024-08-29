# Import the functions from excel_utils.py
from excel_utils import fetch_data_from_excel, update_excel_data
from gdrive import upload_file_to_gdrive, download_file_from_gdrive
from enum import Enum
from sheet import SystemFields
import shutil

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
    print(f"Fetched data: {data[row][col]}")
    if data[row][col] == "Running":
        return False
    else:
        return True

def update_all_system_info(file_path):
    data = fetch_data_from_excel(file_path, sheet_name="System Info")

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
    #update_all_system_info(dload_sysfile_name)
    upload_file_to_gdrive(tmp_stkfile_name)



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
