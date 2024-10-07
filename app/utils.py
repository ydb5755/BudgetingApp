import os
import datetime
import calendar

def get_month_timestamps(month:int, year:int) -> tuple[float, float]:
    print(month, year)
    # Get the first day of the requested month and subtract one day to get the last day of the previous month
    first_day_of_requested_month = datetime.datetime(year, month, 1)
    last_day_of_requested_month = first_day_of_requested_month + datetime.timedelta(days=calendar.monthrange(year, month)[1] - 1) 

    # Convert both datetime objects to timestamps
    first_day_timestamp = first_day_of_requested_month.timestamp()
    last_day_timestamp = datetime.datetime(last_day_of_requested_month.year, last_day_of_requested_month.month, last_day_of_requested_month.day, 23, 59, 59).timestamp()
    return first_day_timestamp, last_day_timestamp

def get_uploads_path() -> str:
    path1 = 'C:/Users/Lenovo/Desktop/BudgetingApp/app/static/uploadable/'
    path2 = '/home/yisroel2/Desktop/budgetingApp/app/static/uploadable/'
    for p in [path1, path2]:
        if os.path.exists(p):
            path = p
            break
    return path