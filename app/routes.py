from app import app, db
from flask import render_template, redirect, url_for, request, jsonify
from sqlalchemy import select, delete, update
from .models import LineItem, BudgetCategory, Vendor
from .utils import get_bank_statements_path, get_month_timestamps, get_all_months
import datetime
import os
import openpyxl
import time

@app.route('/')
def base_url():
    return redirect(url_for('line_items_by_month'))

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

@app.route('/budget_monthly_analysis')
def budget_monthly_analysis():
    all_months = get_all_months()
    return render_template('budget_monthly_analysis.html',
                           all_months=all_months)

@app.route('/line_items_by_month')
def line_items_by_month():
    all_months = get_all_months()
    files = os.listdir(get_bank_statements_path())
    return render_template('line_items_by_month.html', 
                           files=files,
                           all_months=all_months)

@app.route('/upload_bank_statement/<filename>')
def upload_bank_statement(filename:str):
    bank_statement_file_path = get_bank_statements_path() + filename
    xl = openpyxl.load_workbook(bank_statement_file_path, read_only=True)
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

@app.route('/split_line/<line_item_id>')
def split_line(line_item_id):
    existing_child_lines = db.session.execute(select(LineItem).where(LineItem.parent_line_item_id == line_item_id)).scalars()
    li = db.session.execute(select(LineItem).where(LineItem.id == line_item_id)).scalar()
    return render_template('split_line.html',
                           li=li,
                           existing_child_lines=existing_child_lines)

@app.route('/import_file_selector/<line_item_id>')
def import_file_selector(line_item_id):
    li = db.session.execute(select(LineItem).where(LineItem.id == line_item_id)).scalar()
    files = os.listdir('app\static\Credit_Card_Statements')
    return render_template('import_file_selector.html',
                           li=li,
                           files=files)

@app.route('/upload_file_for_line_split/<file_name>/<line_item_id>')
def upload_file_for_line_split(file_name, line_item_id):
    file_path = f'C:/Users/Lenovo/Desktop/BudgetingApp/app/static/Credit_Card_Statements/{file_name}'
    parent_line_item = db.session.execute(select(LineItem).where(LineItem.id == line_item_id)).scalar()
    
    xl = openpyxl.load_workbook(file_path, read_only=True)
    wb = xl.worksheets[0]

    vendors = db.session.execute(select(Vendor.name)).all()
    vendors_added = [vendor[0] for vendor in vendors]
    
    items_to_add = []

    for line, row in enumerate(wb.rows):
        row = [x.value for x in row]
        if line == 0:
            columns = {x: i for i,x in enumerate(row)}
            continue

        if not row[columns['Vendor']] in vendors_added:
            vendors_added.append(row[columns['Vendor']])
            vendor = Vendor(
                name=row[columns['Vendor']]
            )
            db.session.add(vendor)
            db.session.commit()
        vendor_id = db.session.execute(select(Vendor.id).where(Vendor.name==row[columns['Vendor']])).scalar()
        line_item = LineItem(
            parent_line_item_id=line_item_id,
            amount=row[columns['Amount']] * -1,
            currency_type='shekel',
            vendor_id=vendor_id,
            date=parent_line_item.date,
            confirmation_code=row[columns['Confirmation Code']],
            note=None
        )
        items_to_add.append(line_item)
    xl.close()

    db.session.add_all(items_to_add)
    db.session.commit()
    os.remove(file_path)

    return redirect(url_for('split_line', line_item_id=line_item_id))


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
    
@app.route('/add_line_item', methods=['POST'])
def add_line_item():
    if request.method == 'POST':
        date = datetime.datetime.strptime(request.form['Date'], '%Y-%m-%d').timestamp()
        vendor = db.session.execute(select(Vendor).where(Vendor.name == request.form['Vendor'])).scalar()
        if not vendor:
            db.session.add(Vendor(name=request.form['Vendor']))
            db.session.commit()
            vendor = db.session.execute(select(Vendor).where(Vendor.name == request.form['Vendor'])).scalar()
        db.session.add(
            LineItem(
                parent_line_item_id =request.form['ParentId'],
                amount              =request.form['Amount'],
                currency_type       =request.form['Currency-Type'],
                vendor_id           =vendor.id,
                date                =date,
                confirmation_code   =request.form['Confirmation Code'],
                note                =request.form['Note']
            )
        )
        db.session.commit()
        return redirect(url_for('line_items_by_month'))

@app.route('/delete_line_item/<id>', methods=['POST'])
def delete_line_item(id):
    if request.method == 'POST':
        db.session.execute(delete(LineItem).where(LineItem.id==id))
        db.session.commit()
        return redirect(url_for('line_items_by_month'))

@app.route('/add_vendor', methods=['POST'])
def add_vendor():
    if request.method == 'POST':
        
        vendor_name = request.form['vendor_name']
        vendor = Vendor(name=vendor_name)
        db.session.add(vendor)
        db.session.commit()
        return redirect(url_for('vendors'))

@app.route('/update_vendor/<li_id>/<new_name>', methods=['POST'])
def update_vendor(li_id, new_name):
    vendor = db.session.execute(select(Vendor).where(Vendor.name == new_name)).scalar()
    if not vendor:
        db.session.add(Vendor(name=new_name))
        db.session.commit()
    vendor = db.session.execute(select(Vendor).where(Vendor.name == new_name)).scalar()
    db.session.execute(update(LineItem).where(LineItem.id==li_id).values(vendor_id=vendor.id))
    db.session.commit()
    return {"status":'success'}

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
    month_line_items = db.session.execute(select(LineItem).where(LineItem.date > first_day_timestamp, LineItem.date < last_day_timestamp)).scalars().all()
    line_item_list = []
    for li in month_line_items:
        line_item_data = {
            'id':li.id,
            'parent_line_item_id':li.parent_line_item_id,
            'amount':li.amount,
            'currency_type':li.currency_type,
            'vendor':li.get_vendor().name,
            'date':li.display_date(),
            'confirmation_code':li.confirmation_code,
            'note':li.note
        }
        line_item_list.append(line_item_data)
    return jsonify(line_item_list)

@app.route('/update_vendors_budget_category/<vendor_id>/<updated_budget_name>', methods=['POST'])
def update_vendors_budget_category(vendor_id, updated_budget_name):
    budget_cat = db.session.execute(select(BudgetCategory).where(BudgetCategory.name == updated_budget_name)).scalar()
    vendor = db.session.execute(select(Vendor).where(Vendor.id ==vendor_id)).all()
    if budget_cat:
        db.session.execute(update(Vendor).values(bc_id=budget_cat.id).where(Vendor.id==vendor_id))
        db.session.commit()
    else:
        db.session.add(BudgetCategory(
            name=updated_budget_name
        ))
        db.session.commit()

        budget_cat = db.session.execute(select(BudgetCategory).where(BudgetCategory.name == updated_budget_name)).scalar()
        db.session.execute(update(Vendor).values(bc_id=budget_cat.id).where(Vendor.id==vendor_id))
        db.session.commit()


    return {"status":'success'}

    
@app.route('/split_line_endpoint', methods=['POST'])
def split_line_endpoint():
    if not request.method == 'POST':
        return
    
    list_of_items = []
    item_holder = []
    
    for i, v in enumerate(request.form.values()):
        if i == 0:
            parent_id = v
        elif i == 1:
            date = v
        else:
            item_holder.append(v)
            if len(item_holder) == 4:
                list_of_items.append(item_holder.copy())
                item_holder.clear()
    for item in list_of_items:
        vendor_id = db.session.execute(select(Vendor.id).where(Vendor.name==item[1])).scalar()
        if not vendor_id:
            db.session.add(Vendor(name=item[1]))
            db.session.commit()
            vendor_id = db.session.execute(select(Vendor.id).where(Vendor.name==item[1])).scalar()
        db.session.add(LineItem(
            parent_line_item_id = parent_id,
            amount = item[0],
            vendor_id = vendor_id,
            date = date,
            confirmation_code = item[2],
            note = item[3]
        ))
    db.session.commit()


    return redirect(url_for('line_items_by_month'))

@app.route('/get_budget_details_for_month/<month>/<year>', methods=['POST'])
def get_budget_details_for_month(month:str, year:str):
    year = int(year)
    month_int = datetime.datetime.strptime(month, "%b").month
    budgets = db.session.execute(select(BudgetCategory)).scalars().all()
    budget_list = []
    for budget in budgets:
        budget_list.append({
            'id':budget.id,
            'name':budget.name,
            'month_cost':budget.get_total_month_cost(month_int, year)
        })
    return jsonify(budget_list)
