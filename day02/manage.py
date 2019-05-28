
from flask import Flask, request, render_template, session, redirect
from flask_script import Manager


app = Flask(__name__)

app.secret_key = 'w1314ewgdfdsaewqr43ytfdd'

@app.route('/index/')
def index():
    return 'index'


# session的使用：两种方式
#     一、将数据保存在浏览器（客户端）
#     二、将数据保存在服务器（数据库）

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 模拟登陆（session使用）
        username = request.form.get('username')
        passwprd = request.form.get('password')
        if username == 'coco' and passwprd == '123456':
            # 在django中，session[key] = value实际上做了两步操作
            # 第一步：才cookie中设置了键值对，
            session['username'] = 'coco'
            return redirect('/index/')
        return render_template('login.html')


if __name__ == '__name__':
    manage = Manager(app)
    manage.run()