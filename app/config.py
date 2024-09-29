
config = {
    'SQLALCHEMY_DATABASE_URI_SQLITE': 'sqlite:///site.db',
    'SECRET_KEY': '1234567890'
}

class Config():
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI_SQLITE')
    SECRET_KEY              = config.get('SECRET_KEY')