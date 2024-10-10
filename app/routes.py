from app import app, db
from flask import render_template, redirect, url_for, request, jsonify
from sqlalchemy import select, delete, update
from .models import LineItem, BudgetCategory, Vendor
from .utils import get_uploads_path, get_month_timestamps, get_all_months
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
    all_months = get_all_months()
    files = os.listdir(get_uploads_path())
    return render_template('homepage.html', 
                           files=files,
                           all_months=all_months)

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



###################
# API calls below #
###################


@app.route('/add_budget_category', methods=['POST'])
def add_budget_category():
    if request.method == 'POST':
        
        category_name = request.form['category_name']
        bc = BudgetCategory(name=category_name)
        db.session.add(bc)
        db.session.commit()
        return redirect(url_for('budget_categories'))
    
    
@app.route('/add_vendor', methods=['POST'])
def add_vendor():
    if request.method == 'POST':
        
        vendor_name = request.form['vendor_name']
        vendor = Vendor(name=vendor_name)
        db.session.add(vendor)
        db.session.commit()
        return redirect(url_for('vendors'))

@app.route('/delete_budget_category/<id>', methods=['POST'])
def delete_budget_category(id):
    db.session.execute(update(Vendor).where(Vendor.bc_id==id).values(bc_id=None))
    db.session.execute(delete(BudgetCategory).where(BudgetCategory.id==id))
    db.session.commit()
    return {"status":'success'}

@app.route('/delete_vendor/<id>', methods=['POST'])
def delete_vendor(id):
    db.session.execute(delete(Vendor).where(Vendor.id==id))
    db.session.commit()
    return {"status":'success'}

@app.route('/get_month_line_items/<month>/<year>', methods=['POST'])
def get_month_line_items(month:str, year:str):
    year = int(year)
    month_int = datetime.datetime.strptime(month, "%b").month
    first_day_timestamp, last_day_timestamp = get_month_timestamps(month_int, year)
    month_line_items = db.session.execute(select(LineItem).where(LineItem.date > first_day_timestamp, LineItem.date < last_day_timestamp)).all()
    line_item_list = []
    for li in month_line_items:
        li = li[0]
        dt_object = datetime.datetime.fromtimestamp(li.date)
        date_string = dt_object.strftime('%Y-%m-%d')
        
        line_item_data = {
            'id':li.id,
            'parent_line_item_id':li.parent_line_item_id,
            'amount':li.amount,
            'currency_type':li.currency_type,
            'vendor':li.get_vendor()[0].name,
            'date':date_string,
            'confirmation_code':li.confirmation_code,
            'note':li.note
        }
        line_item_list.append(line_item_data)
    return jsonify(line_item_list)

@app.route('/update_vendors_budget_category/<vendor_id>/<updated_budget_name>', methods=['POST'])
def update_vendors_budget_category(vendor_id, updated_budget_name):
    db.session.execute(update(Vendor).values().where(id=vendor_id))
    return {"status":'success'}

    