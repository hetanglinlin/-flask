import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from user.views import blue

app = Flask(__name__)

# 设置secret_key
app.secret_key = 'o[ayfosjnfhw487-q9ruq[aek'

# 设置flask-session的内容，将session数据保存在redis中
app.config['SESSION_TYPE'] = 'redis'
# redis.Redis(host='127.0.0.1', port=6379, password='密码')
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
# 初始化Session的两种方式:
# 第一种方式
Session(app)
# 第二种方式
# sess = Session()
# sess.init_app(app)

# 第三步: 注册蓝图
app.register_blueprint(blueprint=blue, url_prefix='/user')

if __name__ == '__main__':
    manage = Manager(app)
    manage.run()