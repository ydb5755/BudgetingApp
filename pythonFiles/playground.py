import datetime
import openpyxl
import time
from sqlalchemy import create_engine, MetaData, Table, select, distinct, extract
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

        x = conn.execute(select(line_item_table.c.date)).all()
        print(x)
        # lis = [datetime.datetime.fromtimestamp(s) for s in conn.execute(select(distinct(line_item_table.c.date))).scalars().all()]
        # month_year = {(s.month, s.year) for s in lis}
        
        # month_year = [datetime.datetime(year=x[1], month=x[0], day=1) for x in month_year]
        # month_year.sort()
        # return [x.strftime("%b %Y") for x in month_year]

if __name__ == '__main__':
    # print(playground())
    print(datetime.datetime.strptime('Aug', "%b").month)