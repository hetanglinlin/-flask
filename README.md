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

