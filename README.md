### flask与django对比引入
### flask最小应用与flask_script的使用
### 路由器规则/请求与响应
### cookie的使用(模拟登录)
### 登录状态校验装饰器
![](https://github.com/hetanglinlin/-flask/blob/master/images/Xmind/day01.png)

### 模板
### 重定向
### 使用蓝图管理路由
### session
    # 使用蓝图管理路由
    # 第一步: 获取蓝图对象
    blue = Blueprint('first', __name__)
    
    # 第二步: 使用蓝图对象管理路由，蓝图对象.route(路由地址)   
    @blue.route('/index/')
    @login_required
    def index():
        return render_template('index.html')

    # 第三步: 注册蓝图
    app.register_blueprint(blueprint=blue, url_prefix='/user')
    
---
    
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
![](https://github.com/hetanglinlin/-flask/blob/master/images/Xmind/day02.png)

### 模板继承与拆分，静态资源加载url_for
### super语法、for循环、通过下标获取数据
### if语法、ifequal语法、宏定义macro语法
### 过滤器
### flask-sqlalchemy的使用，模型的定义，数据库连接地址的配置
### 初始化数据库中的表
### 添加数据add和add_all
### 删除数据delete和修改数据
    class Student(db.Model):
        # 自增的主键id字段
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        # 唯一且不能为空且长度不超过10字符的name字段
        s_name = db.Column(db.String(10), unique=True, nullable=False)
        # 默认为18的age字段
        s_age = db.Column(db.Integer, default=18)
    
        # django: auto_now_add auto_now
        # 只在save()方法调用时auto_now字段才做更新。
        # update()方法调用时auto_now字段不更新
        create_time = db.Column(db.DateTime, default=datetime.now)
    
        # 定义tablename表示模型迁移到数据库中对应的表名称
        # 如果没定义tablename参数，表名为模型名称小写
        __tablename__ = 'stu'
    
        def save(self):
            db.session.add(self)
            db.session.commit()
            
---

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
![](https://github.com/hetanglinlin/-flask/blob/master/images/Xmind/day03.png)

#### 查询filter_by、filter、get
#### 查询order_by、offset、limit、paginate分页
#### 模糊查询comtains、startswith、endswith、like、gt、lt、ge、le
#### 查询and_、or_、not_、in_、notin_
#### 一对多的模型定义与SQL
#### 一对多的模型数据添加、一查多、多查一
#### 多对对模型定于与数据插入
#### 多对多中间表数据的添加append与删除remove
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
        
---

    class Grade(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        g_name = db.Column(db.String(10), nullable=True)
        # 定义模型Grade和Student模型的关联关系
        # relationship可定义在模型的任何一方都可以
        stus = db.relationship('Student', backref='g', lazy=False)
    
        __tablename__ = 'grade'
    
    
    c_s = db.Table('c_s',
       db.Column('c_id', db.Integer, db.ForeignKey('course.id')),
       db.Column('s_id', db.Integer, db.ForeignKey('stu.id'))
    )
    
    
    class Course(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        c_name = db.Column(db.String(10), nullable=False)
        # 指定Course和Student的多对多关联关系
        # relationship可定义在关联模型的任何一方
        stus = db.relationship('Student', secondary=c_s,
                               backref='cou', lazy='dynamic')
    
        __tablename__ = 'course'


    class Student(db.Model):
        # 自增的主键id字段
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        # 唯一且不能为空且长度不超过10字符的name字段
        s_name = db.Column(db.String(10), unique=True, nullable=False)
        # 默认为18的age字段
        s_age = db.Column(db.Integer, default=18)
    
        # django: auto_now_add auto_now
        # 只在save()方法调用时auto_now字段才做更新。
        # update()方法调用时auto_now字段不更新
        create_time = db.Column(db.DateTime, default=datetime.now)
    
        # 定义外键
        # sql: alter table stu add grade_id int;
        # sql: alter table stu add foreign key(grade_id) references grade(id)
        grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)
    
        # 定义tablename表示模型迁移到数据库中对应的表名称
        # 如果没定义tablename参数，表名为模型名称小写
        __tablename__ = 'stu'
![](https://github.com/hetanglinlin/-flask/blob/master/images/Xmind/day04.png)

### 注册表单form定义、错误信息解析、csrf_token定义
### 表单字段的长度校验、密码EqualTo校验、validate_字段、加密解密等等
### 上传图片
### 修改模板和静态文件内容
    @blue.route('/register/', methods=['GET', 'POST'])
    def register():
        form = UserRegisterForm()
    
        if request.method == 'GET':
            return render_template('register.html', form=form)
    
        if request.method == 'POST':
            # 校验传递的username，pw1，pw2是必填值，且长度要限制，账号是否存在判断
            # 1. 定义form表单
            if form.validate_on_submit():
                # 账号密码全部校验成功
                username = form.username.data
                password = form.pw1.data
                icon = form.icon.data
                # 保存账号信息
                user = User()
                user.username = username
                user.password = generate_password_hash(password)
                if icon:
                    # 保存图片，且保存图片字段
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    STATIC_DIR = os.path.join(BASE_DIR, 'static')
                    MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
                    # 保存图片的绝对路径
                    icon_path = os.path.join(MEDIA_DIR, icon.filename)
                    icon.save(icon_path)
                    # 保存图片的相对路径
                    user.icons = icon.filename
    
                db.session.add(user)
                db.session.commit()
            return render_template('register.html', form=form)