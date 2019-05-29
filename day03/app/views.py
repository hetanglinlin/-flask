from flask import Blueprint, render_template, request

from app.models import db, Student

blue = Blueprint('app', __name__)


@blue.route('/index/', methods=['GET'])
def index():
    item1 = ['django', 'flask', 'tornado', 'vue', 'docker',
             'linux', 'mysql', 'redis', 'mongodb', 'celery',
             'rabbitmq', 'git']
    content_h2 = '<h2>我是h2标签</h2>'
    return render_template('index.html', item1=item1,
                           content_h2=content_h2)


@blue.route('/index1/', methods=['GET'])
def index1():
    return render_template('index1.html')


@blue.route('/init_db/', methods=['GET'])
def init_db():
    # 将模型映射成表，只用使用一次
    db.create_all()
    # db.drop_all()
    return '初始化数据库成功'


@blue.route('/stu/', methods=['POST', 'DELETE', 'PATCH'])
def stu():
    if request.method == 'POST':
        # 创建学生表数据
        stu = Student()
        stu.s_name = '小明'
        # 事务session的add方法，其实是在准备插入语句insert
        # db.session.add(stu)
        # 事务session提交了，数据才会插入到数据库中
        # db.session.commit()
        # 优化保存方法，stu.save()
        stu.save()
        return '插入单条数据成功'

    if request.method == 'DELETE':
        stu = Student.query.filter(Student.s_name == '王五3').first()
        stu = Student.query.filter_by(s_name='李四2').first()
        # delete(接收删除对象)
        db.session.delete(stu)
        db.session.commit()
        return '删除数据成功'

    if request.method == 'PATCH':
        stu = Student.query.filter(Student.s_name == '小明').first()
        stu.s_age = 22
        # 修改和创建可以调用db.session.add() 和commit()操作
        # stu.save()
        db.session.commit()
        return '修改数据成功'


@blue.route('/stus/', methods=['GET'])
def stus():
    names = ['张三1', '李四2', '王五3']
    stus_list = []
    for name in names:
        stu = Student()
        stu.s_name = name
        # stu.save()
        stus_list.append(stu)
    # add_all([添加对象1, 添加对象2....])
    db.session.add_all(stus_list)
    db.session.commit()
    return '批量插入数据成功'


