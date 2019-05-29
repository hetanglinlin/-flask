from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
