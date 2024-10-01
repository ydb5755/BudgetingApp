from app import app, db
from flask import render_template, redirect, url_for, request
from sqlalchemy import select, delete, update
from app.models import LineItem, BudgetCategory, Vendor
import datetime
import os
import openpyxl
import time
import calendar

def get_uploads_path() -> str:
    path1 = 'C:/Users/Lenovo/Desktop/BudgetingApp/app/static/uploadable/'
    path2 = '/home/yisroel2/Desktop/budgetingApp/app/static/uploadable/'
    for p in [path1, path2]:
        if os.path.exists(p):
            path = p
            break
    return path

@app.route('/')
def home():
    # Get the current date
    now = datetime.datetime.now()

    # Get the first day of the current month and subtract one day to get the last day of the previous month
    first_day_of_current_month = datetime.datetime(now.year, now.month, 1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)

    # Get the first day of the previous month
    first_day_of_previous_month = datetime.datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)

    # Convert both datetime objects to timestamps
    first_day_timestamp = first_day_of_previous_month.timestamp()
    last_day_timestamp = datetime.datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, last_day_of_previous_month.day, 23, 59, 59).timestamp()

    all_line_items = db.session.execute(select(LineItem).where(LineItem.date > first_day_timestamp, LineItem.date < last_day_timestamp)).all()
    for li in all_line_items:
        dt_object = datetime.datetime.fromtimestamp(li[0].date)
        date_string = dt_object.strftime('%Y-%m-%d')
        li[0].date = date_string
    vendors = db.session.execute(select(Vendor)).all()
    budget_categories = db.session.execute(select(BudgetCategory)).all()
    files = os.listdir(get_uploads_path())
    return render_template('index.html', 
                           files=files,
                           vendors=vendors,
                           budget_categories=budget_categories,
                           all_line_items=all_line_items)

@app.route('/upload_file/<filename>')
def upload_file(filename:str):
    file_path = get_uploads_path() + filename
    xl = openpyxl.load_workbook(file_path, read_only=True)
    wb = xl.worksheets[0]
    
    items_to_add = []
    
    vendors = db.session.execute(select(Vendor.name)).all()
    vendors_added = [vendor[0] for vendor in vendors]
    
    for line, row in enumerate(wb.rows):
        row = [x.value for x in row]
        if line == 0:
            columns = {x: i for i,x in enumerate(row)}
            continue
        if row[columns['Charge']]:
            amount=row[columns['Charge']] * -1
        else:
            amount=row[columns['Deposit']]
        
        date = row[0]
        date = time.mktime(date.timetuple())

        if not row[columns['Vendor']] in vendors_added:
            vendors_added.append(row[columns['Vendor']])
            vendor = Vendor(
                name=row[columns['Vendor']]
            )
            db.session.add(vendor)
            db.session.commit()
        vendor_id = db.session.execute(select(Vendor.id).where(Vendor.name==row[columns['Vendor']])).scalar()
        line_item = LineItem(
            parent_line_item_id=None,
            amount=amount,
            currency_type='shekel',
            vendor_id=vendor_id,
            date=date,
            confirmation_code=row[columns['Confirmation Code']],
            note=row[columns['Note']]
        )
        items_to_add.append(line_item)

    xl.close()

    db.session.add_all(items_to_add)
    db.session.commit()

    # os.remove(file_path)
    return redirect(url_for('home'))

@app.route('/view_month/<year>/<month>')
def view_month(year, month):
    return render_template('view_month.html',
                           month=month,
                           year=year)

@app.route('/add_budget_category', methods=['POST'])
def add_budget_category():
    if request.method == 'POST':
        
        category_name = request.form['category_name']
        bc = BudgetCategory(name=category_name)
        db.session.add(bc)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/delete_budget_category/<id>', methods=['POST'])
def delete_budget_category(id):
    db.session.execute(update(Vendor).where(Vendor.bc_id==id).values(bc_id=None))
    db.session.execute(delete(BudgetCategory).where(BudgetCategory.id==id))
    db.session.commit()
    return {"status":'success'}