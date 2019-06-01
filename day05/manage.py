import os

from flask import Flask
from flask_script import Manager

from app.models import db
from app.views import blue

# BASE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.join(BASE_DIR, 'app'), 'static')
TEMPLATE_DIR = os.path.join(os.path.join(BASE_DIR, 'app'), 'templates')

# app = Flask(__name__,
#             template_folder=TEMPLATE_DIR,
#             static_folder=STATIC_DIR)

app = Flask(__name__,
            template_folder='app/templates/',
            static_folder='app/static/')

# 在session中会使用，在表单wtf中生成csrf也会使用
app.secret_key = 'asdhgqr8230rifhslzmxcn'
app.register_blueprint(blueprint=blue, url_prefix='/app')

# 数据库配置
# mysql+pymysql://root:password@127.0.0.1:3306/flask1901
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/flask1901'
db.init_app(app)


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()




