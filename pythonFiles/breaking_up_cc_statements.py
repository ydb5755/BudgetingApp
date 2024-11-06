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
    lines_to_skip = []
    for row_num, row in enumerate(data):
        if row[0] == card:
            if data[row_num + 1][0] == 'אין נתונים להצגה':
                return None
            start = row_num + 3
            break
    for row_num, row in enumerate(data[start + 1:]):
        if row[0] in card_names:
            end = row_num - 2
            break
    for row_num, row in enumerate(data[start:end]):
        if row[0] == 'עסקאות בחו˝ל':
            lines_to_skip = list(range(row_num - 1, row_num + 2))
            # for chul_line_num, chul_line in enumerate(data[row_num:end]):
            #     if chul_line[0] == None:
            #         lines_to_skip.append(chul_line_num)
    if end == None:
        end = len(data)
        
    if start and end:
        new_file_name = name_file(og_file=file, card_num=card_num)
        build_new_file(new_file_name, data[start:end])
    
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

def build_new_file(name_of_new_file:str, list_of_rows:list[str]):
    new_columns_with_indexes = {'Amount':4, 'Vendor':1, 'Confirmation Code':6}
    results = []
    for row in list_of_rows:
        if row[new_columns_with_indexes['Amount']] == 0:
            continue
        relevant_values = []
        for index in new_columns_with_indexes.values():
            relevant_values.append(row[index])
        results.append(relevant_values)
    if confirm_has_values(relevant_values):
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(results, columns=['Amount', 'Vendor', 'Confirmation Code'])

        # Write the DataFrame to an Excel file
        df.to_excel(f'{target_dir}/{name_of_new_file}', index=False)

if __name__ == '__main__':
    print(list(range(4,6)))
    # process_file(target_file)
    