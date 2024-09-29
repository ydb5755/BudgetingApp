import datetime
import openpyxl
import time
from sqlalchemy import create_engine, MetaData, Table, select
import os

def engineer():
    path1 = 'C:/Users/Lenovo/Desktop/BudgetingApp/instance/site.db'
    path2 = '/home/yisroel2/Desktop/budgetingApp/instance/site.db'
    # path3 = ''

    for p in [path1, path2]:
        if os.path.exists(p):
            path = p
            break
    engine = create_engine(f'sqlite:///{path}')
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    return engine, metadata_obj

def playground():
    engine, metadata_obj = engineer()
    line_item_table = Table("line_item", metadata_obj, autoload_with=engine)
    budget_category_table = Table("budget_category", metadata_obj, autoload_with=engine)
    vendor_table = Table("vendor", metadata_obj, autoload_with=engine)

    with engine.connect() as conn:
        lis = conn.execute(select(line_item_table))

    # xl = openpyxl.load_workbook('C:/Users/Lenovo/Desktop/BudgetingApp/app/static/uploadable/Bulk_Line_Item_Upload.xlsx',read_only=True)
    # wb = xl.worksheets[0]
    # items_to_add = []
    # for line, row in enumerate(wb.rows):
    #     row = [x.value for x in row]
    #     if line == 0:
    #         columns = {x: i for i,x in enumerate(row)}
    #         continue
    #     if row[columns['Charge']]:
    #         amount=row[columns['Charge']] * -1
    #     else:
    #         amount=row[columns['Deposit']]
    #     date = row[0]
    #     date = time.mktime(date.timetuple())
    #     line_item = {
    #         'parent_line_item_id':None,
    #         'amount':amount,
    #         'currency_type':'shekel',
    #         'vendor_id':None,
    #         'date':date,
    #         'confirmation_code':row[columns['Confirmation Code']],
    #         'note':row[columns['Note']]
    #     }
    #     items_to_add.append(line_item)
    # print(len(items_to_add))
    # print(items_to_add[51])

    # month = datetime.datetime.now().date().month
    # year = datetime.datetime.now().date().year
    # print(month)
    # print(year)
    # print(type(month))
    # print(type(year))
    # print(datetime.datetime.now(datetime.timezone.utc).timestamp())
    
    # today = datetime.datetime.today().date()
    # today = time.mktime(today.timetuple())
    # print(today)

if __name__ == '__main__':
    playground()