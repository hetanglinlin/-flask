from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '< Student (%s) >' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(255))
    icons = db.Column(db.String(50))

    __tablename__ = 'user'
