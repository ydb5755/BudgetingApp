from app import db
from sqlalchemy import Column, INTEGER, String

class Vendor(db.Model):
    __tablename__ = 'vendor'
    id            = Column('id', INTEGER(), primary_key=True)
    name          = Column('name', String(), nullable=False)
    bc_id         = Column('bc_id', INTEGER(), nullable=True)

class BudgetCategory(db.Model):
    __tablename__ = 'budget_category'
    id            = Column('id', INTEGER(), primary_key=True)
    name          = Column('name', String(), nullable=False)

class LineItem(db.Model):
    __tablename__       = 'line_item'
    id                  = Column('id', INTEGER(), primary_key=True)
    parent_line_item_id = Column('parent_line_item_id', INTEGER(), nullable=True)
    amount              = Column('amount', INTEGER(), nullable=False)
    currency_type       = Column('currency_type', String(), default='shekel')
    vendor_id           = Column('vendor_id', INTEGER(), nullable=True)
    date                = Column('date', INTEGER(), nullable=False)
    confirmation_code   = Column('confirmation_code', INTEGER(), nullable=True)
    note                = Column('note', String(), nullable=True)

