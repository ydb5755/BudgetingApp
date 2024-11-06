from app import db
from sqlalchemy import Column, INTEGER, String, select, distinct
import datetime
class Vendor(db.Model):
    __tablename__ = 'vendor'
    id            = Column('id', INTEGER(), primary_key=True, autoincrement=True)
    name          = Column('name', String(), nullable=False)
    bc_id         = Column('bc_id', INTEGER(), nullable=True)

    def get_budget_category(self):
        return db.session.execute(select(BudgetCategory).where(BudgetCategory.id==self.bc_id)).scalar()
    
    def get_line_items(self):
        return db.session.execute(select(LineItem).where(LineItem.vendor_id==self.id)).scalars().all()
    
    def __repr__(self) -> str:
        return f'{self.name}'

class BudgetCategory(db.Model):
    __tablename__ = 'budget_category'
    id            = Column('id', INTEGER(), primary_key=True, autoincrement=True)
    name          = Column('name', String(), nullable=False)

    def get_vendors(self):
        return db.session.execute(select(Vendor).where(Vendor.bc_id==self.id)).scalars().all()

    def get_line_items(self):
        line_items = []
        vendors = self.get_vendors()
        for vendor in vendors:
            line_items += vendor.get_line_items()
        return line_items
    
    def get_total_month_cost(self, month:int, year:int):
        from .utils import get_month_timestamps
        first_ts, last_ts = get_month_timestamps(month, year)
        line_items = self.get_line_items()
        x = list(db.session.execute(select(distinct(LineItem.parent_line_item_id))).scalars().all())
        if None in x:
            x.remove(None)
        requested_month_lis = 0
        for li in line_items:
            if first_ts < li.date < last_ts and not li.id in x:
                requested_month_lis += li.amount
            elif first_ts < li.date < last_ts:
                print(li.amount)
        return requested_month_lis

    
class LineItem(db.Model):
    __tablename__       = 'line_item'
    id                  = Column('id', INTEGER(), primary_key=True, autoincrement=True)
    parent_line_item_id = Column('parent_line_item_id', INTEGER(), nullable=True)
    amount              = Column('amount', INTEGER(), nullable=False)
    currency_type       = Column('currency_type', String(), default='shekel')
    vendor_id           = Column('vendor_id', INTEGER(), nullable=True)
    date                = Column('date', INTEGER(), nullable=False)
    confirmation_code   = Column('confirmation_code', INTEGER(), nullable=True)
    note                = Column('note', String(), nullable=True)

    def get_parent_line(self):
        return db.session.execute(select(LineItem).where(LineItem.id==self.parent_line_item_id)).scalar()
    
    def get_children_lines(self):
        return db.session.execute(select(LineItem).where(LineItem.parent_line_item_id==self.id)).all()

    def get_vendor(self):
        return db.session.execute(select(Vendor).where(Vendor.id==self.vendor_id)).scalar()
    
    def display_date(self):
        dt_object = datetime.datetime.fromtimestamp(self.date)
        return dt_object.strftime('%Y-%m-%d')