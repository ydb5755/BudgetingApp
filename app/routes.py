from app import app, db
from flask import render_template, redirect, url_for, request
from sqlalchemy import select, delete, update
from .models import LineItem, BudgetCategory, Vendor
from .utils import get_uploads_path, get_month_timestamps
import datetime
import os
import openpyxl
import time

@app.route('/budget_categories')
def budget_categories():
    budget_categories = db.session.execute(select(BudgetCategory)).all()
    return render_template('budget_categories.html',
                           budget_categories=budget_categories)


@app.route('/vendors')
def vendors():
    vendors = db.session.execute(select(Vendor)).all()
    return render_template('vendors.html',
                           vendors=vendors)


@app.route('/')
def home():
    last_month_datetime = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month, 1) - datetime.timedelta(days=1)
    first_day_timestamp, last_day_timestamp = get_month_timestamps(last_month_datetime.month, last_month_datetime.year)
    last_month_lines = db.session.execute(select(LineItem).where(LineItem.date > first_day_timestamp, LineItem.date < last_day_timestamp)).all()
    for li in last_month_lines:
        dt_object = datetime.datetime.fromtimestamp(li[0].date)
        date_string = dt_object.strftime('%Y-%m-%d')
        li[0].date = date_string
    files = os.listdir(get_uploads_path())
    return render_template('homepage.html', 
                           files=files,
                           last_month_lines=last_month_lines)

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
        return redirect(url_for('budget_categories'))

@app.route('/delete_budget_category/<id>', methods=['POST'])
def delete_budget_category(id):
    db.session.execute(update(Vendor).where(Vendor.bc_id==id).values(bc_id=None))
    db.session.execute(delete(BudgetCategory).where(BudgetCategory.id==id))
    db.session.commit()
    return {"status":'success'}