import uuid

from flask import Flask, request, make_response, \
    render_template, redirect
from flask_script import Manager

# 获取flask对象
from day01.utils.functions import login_required

app = Flask(__name__)

# 类似于django中的urls.py文件
# re_path==url, /?P<id>\d+/, path  <int:id>
# django中: <int:name> <str:name> <uuid:name> <path:name>
# flask中: <int:id> <string:name> <uuid:uid>
#          <float:price> <path:pth>

@app.route('/index/')
@login_required
def index():
    # 登录才能访问，没登录不让访问
    # token：1914e7628d3241ffa203001aa0fbdf3d
    # token = request.cookies.get('token')
    # # TODO: 去查询保存token和用户关联关系的表中查询token是否有效
    # if token == '1914e7628d3241ffa203001aa0fbdf3d':
    #     return 'hello flask'
    # return redirect('/login/')
    return 'hello flask'


@app.route('/getid/<int:id>/')
def gid(id):
    print(type(id))
    return 'id:{}'.format(id)

# 定义接受参数时，<转换器(类型):参数名>
# <string:name> 等于 <name>

@app.route('/getstr/<name>/')
def getstr(name):
    print(type(name))
    return 'name:{a}'.format(a=name)


@app.route('/getstr2/<string:name>/')
def getstr2(name):
    print(type(name))
    return 'name:%s' % name


@app.route('/uuid/<uuid:uid>/')
def getuid(uid):
    # 12345678-1234-1234-1234-123456789012
    print(type(uid))
    return 'uid: {}'.format(uid)


@app.route('/getfloat/<float:price>/')
def getprice(price):
    return 'price:{}'.format(price)


@app.route('/getpath/<path:pth>/')
def getpath(pth):
    return 'path:%s' % pth

# 请求与响应
# 请求: request请求上下文


@app.route('/params/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def params():
    # 获取GET请求传递的参数
    if request.method == 'GET':
        # 获取GET传递的参数，使用args
        name = request.args['name']
        name = request.args.get('name')
        names = request.args.getlist('name')
    if request.method == 'POST':
        # 获取POST\PUT\PATCH\DELETE 传递的参数，使用form
        name = request.form['name']
        name = request.form.get('name')
        name = request.form.getlist('name')
    # 获取上传文件
    request.files
    # 获取cookie
    request.cookies
    # 获取路径
    request.path
    # 远程地址
    request.remote_addr

    return '获取参数成功'


@app.route('/res/', methods=['GET'])
def res():
    # django/flask: 响应对象.set_cookie()
    # django中: 响应对象=HttpResponseRedirect()
    # 创建响应对象, make_response('响应内容', '响应状态码')
    html = render_template('index.html')
    response = make_response('<h2>Flask 微型框架</h2>', 200)
    response = make_response(html, 200)
    response.set_cookie('token', 'gasdgiasdgitqr', max_age=10)

    # 响应状态码
    response.status_code
    # 响应内容
    response.data

    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # TODO：获取参数并做字段form表单的校验，使用Flask-wtf
        username = request.form.get('username')
        password = request.form.get('password')
        # django: make_password(), check_password(), md5()
        # flask: generate_password_hash(), check_password_hash()
        if username == 'coco' and password == '123456':
            # 模拟登陆， 使用cookie
            # 1. 向前端的cookie中保存标识符
            res = redirect('/index/')
            token = uuid.uuid4().hex
            res.set_cookie('token', token, max_age=86400)
            # TODO 2. 存储token和用户的关联关系(mysql、redis、mongodb)
            # 跳转（重定向）
            return res


if __name__ == '__main__':
    # 启动程序run()
    # host表示ip
    # port表示端口
    # dedug表示调试模式
    # app.run(host='0.0.0.0', port=8000, debug=True)
    manage = Manager(app)
    # 启动命令修改为: python manage.py runserver -p -h -d
    manage.run()
