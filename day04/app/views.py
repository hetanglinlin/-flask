from flask import Blueprint, render_template, request

from sqlalchemy import and_, or_, not_

from app.models import db, Student, Grade, Course

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


@blue.route('/stu/', methods=['POST', 'DELETE', 'PATCH', 'GET'])
def stu():

    if request.method == 'GET':
        # flask中all()返回的是列表
        # django中all()返回的是queryset， all().first()
        stus = Student.query.all()
        print(stus)
        stus = Student.query.first()
        print(stus)
        stu = Student.query.filter(Student.s_name == '小明').all()[0]
        print(stu)
        stu = Student.query.filter(Student.s_name == '小明').first()
        print(stu)
        stu = Student.query.filter_by(s_name='小明').first()
        print(stu)
        # django中get(s_name='xxxx'): 条件必须成立，通过条件查询返回内容必须唯一
        # flask中get(主键值): 查询主键所在行的数据对象，如果不存在，则返回None
        stu = Student.query.get(1)
        print(stu)

        # order_by
        # django中 Student.objects.all().order_by()
        # stus = Student.query.order_by('-id')
        stus = Student.query.order_by(-Student.id).all()
        print(stus)

        # offset  limit
        page = 1
        start_page = (page - 1) * 2
        stus = Student.query.offset(start_page).limit(2).all()
        print(stus)

        # django： p = Paginator(所有的结果, 条数)  p.page(页码)
        # django： p.next_page_number  p.previous_page_number
        # flask: paginate
        p = Student.query.paginate(page, 2)
        stus = p.items
        # 上一页、下一页
        # 是否有下一页： p.has_next    p.next_num
        # 是否有上一页: p.has_prev    p.prev_num
        print(stus)

        # contains/startswith/endswith/like
        # django中： filter(s_name__contains = '张三‘)
        # contains  like '%张三%'
        stus = Student.query.filter(Student.s_name.contains('张三')).all()
        print(stus)
        # startswith  like '张%' '张_'
        stus = Student.query.filter(Student.s_name.startswith('张')).all()
        print(stus)
        stus = Student.query.filter(Student.s_name.like('张%')).all()
        print(stus)
        stus = Student.query.filter(Student.s_name.like('张_')).all()
        print(stus)

        # gt  ge  lt le   >=  <= <  >
        stus = Student.query.filter(Student.s_age > 18).all()
        print(stus)
        stus = Student.query.filter(Student.s_age.__gt__(18)).all()
        print(stus)

        # 多条件查询
        # django中  filter(Q(), Q())  filter(Q() | Q())  filter(~Q())
        # flask中
        # 多条件且操作
        stus = Student.query.filter(Student.s_age >= 18)\
            .filter(Student.s_name.startswith('张')).all()
        print(stus)
        stus = Student.query.filter(Student.s_age >= 18,
                                    Student.s_name.startswith('张')).all()
        print(stus)
        stus = Student.query.filter(and_(Student.s_age >= 18,
                                        Student.s_name.startswith('张'))).all()
        print(stus)

        # 多条件或操作
        stus = Student.query.filter(or_(Student.s_age > 18,
                                        Student.s_name.startswith('张'))).all()
        print(stus)

        # 多条件非操作
        # [^0-9a-z]
        stus = Student.query.filter(not_(Student.s_age >= 18)).all()
        print(stus)

        # in_  notin_
        stus = Student.query.filter(Student.id.in_([1,2,3])).all()
        print(stus)
        stus = Student.query.filter(Student.id.notin_([1,2,3])).all()
        print(stus)

        return '查询数据成功'

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


@blue.route('/add_grade/', methods=['GET'])
def add_grade():
    names = ['Python班级', 'Java班级', 'Php班级', 'UI班级']
    for name in names:
        g = Grade()
        g.g_name = name
        db.session.add(g)
        db.session.commit()
    return '添加班级信息成功'


@blue.route('/stu_grade/', methods=['GET'])
def stu_grade():
    stus = Student.query.filter(Student.id.in_([1,2,3])).all()
    grade = Grade.query.filter(Grade.g_name == 'Python班级').first()
    for stu in stus:
        # 在django中: grade_id = models.Foreignkey(Grade)
        # stu.grade_id = 班级对象
        # stu.grade_id_id = 班级对象的主键id值
        # 在flask中: grade_id = db.Column(ForeignKey('grade.id'))
        stu.grade_id = grade.id
        stu.save()
    return '分配班级信息成功'


@blue.route('/sel_stu_by_grade/', methods=['GET'])
def sel_stu_by_grade():
    grade = Grade.query.filter(Grade.g_name == 'Python班级').first()
    # 通过班级查询学生信息
    stus = grade.stus
    # 通过学生信息查询班级信息
    stu = stus[0]
    stu_grade = stu.g
    return '查询班级信息成功'


@blue.route('/stu_course/', methods=['GET'])
def stu_course():
    stus = Student.query.filter(Student.id.in_([1,2,3])).all()
    cou = Course.query.filter(Course.c_name == 'VHDL').first()
    # for stu in stus:
    #     # 获取学生对应的课程信息
    #     stu.cou
    #     # 给学生添加课程
    #     stu.cou.append(cou)
    #     # 删除学生的课程
    #     stu.cou.remove(cou)
    for stu in stus:
        # 课程添加学生
        cou.stus.append(stu)

    db.session.commit()
    return '学生添加课程成功'




