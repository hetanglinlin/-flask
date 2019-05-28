from flask import request, render_template, session, \
    redirect, Blueprint, url_for

from utils.functions import login_required

# 场景: 使用蓝图管理路由
# 第一步: 获取蓝图对象
blue = Blueprint('first', __name__)

# 第二步: 使用蓝图对象管理路由，蓝图对象.route(路由地址)

@blue.route('/index/')
@login_required
def index():
    return render_template('index.html')


# session使用: 有两种方式
# 第一种: 将数据保存在浏览器(客户端)
# 第二种: 将数据保存在服务器（数据库）

@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 模拟登陆（讲session使用）
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'coco' and password == '123456':
            # 在django中，session[key] = value实际上做了两步操作
            # 第一步: 在cookie中设置了键值对，键为sessionid，value为随机唯一的字符串
            # 第二步: 在django_session表中session_key字段，这个字段存储的是value值
            #        session_data字段里面存储的是键值对

            # 第一种: 使用flask默认的session存储方式: 将数据保存在cookie中
            # cookie中key为session，value为向session中设置的键值对，如username和coco

            # 第二种: 使用flask-session进行session数据存储方式，将数据保存在redis中
            # 第一步: 当发送任何一个请求到服务器后，服务器会判断当前的会话是否是新的会话，
            #        如果是新会话，则在cookie中设置key为session字符串，value为uuid值
            #        且将uuid值存储在redis中（string类型）
            # 第二步: 向session中存储的键值对，是保存在redis的string类型中的。
            #        不管是想session中设值还是取值，都是中string类型中取的。

            session['username'] = 'coco'
            return redirect('/index/')
        return render_template('login.html')


@blue.route('/stu/<int:id>/')
def stu(id):
    return 'stu id:{}'.format(id)


@blue.route('/stu2/')
def stu2():
    return 'stu'


@blue.route('/stu3/<int:id1>/<int:id2>/<int:id3>/')
def stu3(id1, id2, id3):
    return 'stu3 id1:{} id2:{} id3:{}'.format(id1, id2, id3)

# 反向解析: redirect
# 在django中: redirect('/stu/1/')  redirect('/stu/1/2/3/')
#            redirect(reverse(namespace:name, args=(1,2,3)))
#            redirect(reverse(namespace:name, kwargs={id:1, id2:2, id3:3}))

# 在flask中: redirect('/stu/1/')  redirect('/stu3/1/2/3/')
#           redirect(url_for('生成蓝图对象的第一个参数.重定向函数名',
#                           参数名1=值1, 参数名2=值2。。。。))


@blue.route('/redirect_params/', methods=['GET'])
def redirect_params():
    # 直接定义重定向地址
    # return redirect('/user/stu2/')
    # url_for('生成蓝图的第一个参数.重定向的函数名称')
    # print(url_for('first.stu2'))
    # return redirect(url_for('first.stu2'))
    # print(url_for('first.stu', id=2))
    # return redirect(url_for('first.stu', id=1))
    # return redirect('/user/stu3/1/2/3/')
    print(url_for('first.stu3', id1=1, id2=2, id3=3))
    return redirect(url_for('first.stu3', id1=1, id2=2, id3=3))


@blue.route('/redirect_index/', methods=['GET'])
def redirect_index():

    return redirect(url_for('first.index'))
