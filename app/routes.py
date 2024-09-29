from app import app, db
from flask import render_template, redirect, url_for, request
from sqlalchemy import select, delete, update
from app.models import LineItem, BudgetCategory, Vendor
import datetime
import os
import openpyxl
import time


@app.route('/')
def home():
    this_year = datetime.datetime.now().date().year
    this_month = datetime.datetime.now().date().month
    # line_item_dates = db.session.query(select(LineItem.date).order_by(LineItem.date))
    notes = db.session.execute(select(LineItem.note)).all()
    vendors = db.session.execute(select(Vendor)).all()
    budget_categories = db.session.execute(select(BudgetCategory)).all()
    files = os.listdir('C:/Users/Lenovo/Desktop/BudgetingApp/app/static/uploadable')
    return render_template('index.html', 
                           files=files,
                           notes=notes,
                           vendors=vendors,
                           budget_categories=budget_categories)

@app.route('/upload_file/<filename>')
def upload_file(filename):

    file_path = 'C:/Users/Lenovo/Desktop/BudgetingApp/app/static/uploadable/' + filename
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

        line_item = LineItem(
            parent_line_item_id=None,
            amount=amount,
            currency_type='shekel',
            vendor_id=None,
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