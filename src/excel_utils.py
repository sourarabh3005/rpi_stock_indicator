from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def fetch_data_from_excel(file_path, sheet_name=None):
    # Load the workbook
    workbook = load_workbook(filename=file_path, data_only=True)
    
    # Select the sheet by name or the active sheet by default
    if sheet_name:
        sheet = workbook[sheet_name]
    else:
        sheet = workbook.active
    
    # Fetch data as a list of lists (rows and columns)
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    
    return data

def excel_save(file_path):
    workbook.save(file_path)

def update_excel_data(workbook, sheet_name, row, column, new_value):
    sheet = workbook[sheet_name]
    # Update the specific cell
    sheet.cell(row=row+1, column=column+1, value=new_value)    



def change_row_color(file_path, sheet_name, row, color):
    """
    Change the background color of all cells in a specific row.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet where the row color needs to be changed.
    :param row: Row number (1-based index) to apply the color.
    :param color: Hex color code for the background (default is green).
    """
    # Load the workbook and select the sheet
    workbook = load_workbook(filename=file_path)
    sheet = workbook[sheet_name]
    
    # Create a fill pattern with the specified color
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    
    # Apply the color to all cells in the specified row
    for cell in sheet[row]:
        cell.fill = fill
    
    # Save the workbook
    workbook.save(file_path)
    print(f"Changed the background color of row {row} to {color}")

def change_cell_color(workbook, sheet_name, row, column, color):
    sheet = workbook[sheet_name]
    
    # Create a fill pattern with the specified color
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    
    # Apply the color to the specified cell
    cell = sheet.cell(row=row + 1, column=column + 1)
    cell.fill = fill
    #workbook.save(file_path)
    
    
# Example usage
#file_path = '/home/sourabh/proj/rpi_stock_indicator/tmp/listed_stocks.xlsx'
#data = fetch_data_from_excel(file_path, sheet_name="Sheet1")
#print(data)
#update_excel_data(file_path, sheet_name="Sheet1", row=5, column=5, new_value="hello")
#change_row_color(file_path, sheet_name="Sheet1", row=5, color="FFFF00")
