import os
from openpyxl import load_workbook
import pandas as pd


work_dir = 'C:/Users/Lenovo/Desktop/CC_Statements_xlsx'
target_dir = 'C:/Users/Lenovo/Desktop/Temp_Target'
target_file = 'Export_4_2023.xlsx'
card_names = {'מסטרקארד - 3235':'3235', 'מסטרקארד - 3349':'3349', 'גולד - מסטרקארד - 3047 *':'3047'}

def process_directory():
    dir = os.listdir(work_dir)
    for file in dir:
        process_file(file)

def process_file(file:str):
    wb = load_workbook(f'{work_dir}/{file}')
    
    ws = transform_generator(wb.active)
    
    for card, card_num in card_names.items():
        process_card(card, card_num, file, ws)
        
def process_card(
        card:str, 
        card_num:str, 
        file:str, 
        data:list[list[str]]
):
    start = None
    end = None

    for row_num, row in enumerate(data):
        if row[0] == card:
            if data[row_num + 1][0] == 'אין נתונים להצגה':
                return None
            start = row_num + 3
            break
    for row_num, row in enumerate(data):
        if row[0] in card_names and row_num > start:
            end = row_num - 2
            break
    if end == None:
        end = len(data)
    chul_flag = False
    result = []
    for row_num, row in enumerate(data):
        if start <= row_num < end:
            if row[0] == 'עסקאות בחו˝ל':
                chul_flag = len(result)
            if not row[0]:
                continue
            if chul_flag:
                result.append([row[5], row[2], ''])
            else:
                result.append([row[4], row[1], row[6]])
    if chul_flag:
        del result[chul_flag-1:chul_flag+2]
    new_file_name = name_file(og_file=file, card_num=card_num)
    build_new_file(new_file_name, result)
    
    return True

def name_file(og_file:str, card_num:str):
    name, ext = og_file.split('.')
    name += f'_{card_num}'
    return '.'.join([name, ext])


def transform_generator(ws):
    return [[x.value for x in row] for row in ws.rows]

def confirm_has_values(rows:list):
    total = 0
    for row in rows:
        total += int(row[0])
    return True if total > 0 else False

def build_new_file(name_of_new_file:str, list_of_rows:list[list[str]]):
    if confirm_has_values(list_of_rows):
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(list_of_rows, columns=['Amount', 'Vendor', 'Confirmation Code'])

        # Write the DataFrame to an Excel file
        df.to_excel(f'{target_dir}/{name_of_new_file}', index=False)


def change_excel_version():
    files = ['Export_1_2023.xls', 'Export_1_2024.xls']
    from xls2xlsx import XLS2XLSX
    for file in files:
        f_path = f'{work_dir}/{file}'
        x2x = XLS2XLSX(f_path)
        x2x.to_xlsx(f'{work_dir}/{file}x')

if __name__ == '__main__':
    process_directory()
    