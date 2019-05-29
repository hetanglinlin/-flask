from flask import Flask
from flask_script import Manager

from app.models import db
from app.views import blue

app = Flask(__name__)
app.register_blueprint(blueprint=blue, url_prefix='/app')

# 数据库配置
# mysql+pymysql://root:password@127.0.0.1:3306/flask1901
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/flask1901'
db.init_app(app)


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()




