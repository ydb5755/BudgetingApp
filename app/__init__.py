from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app,db)

from app import models #.models import Vendor, LineItem, BudgetCategory
from app import routes

