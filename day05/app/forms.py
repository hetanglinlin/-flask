from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from app.models import User

# serializer.ModelSerializer /  serialzier.Serializer

class UserRegisterForm(FlaskForm):
    # 校验注册页面传递的username、pw1、pw2三个字段
    # django中: username = form.CharField(required, max_length=10, error_messages={})
    username = StringField('账号', validators=[DataRequired(message='账号必填'),
                                             Length(5,10, message='账号长度只能在5到10位之间')])
    pw1 = StringField('密码', validators=[DataRequired(message='密码必填'),
                                        Length(5,10, message='账号长度只能在5到10位之间')])
    pw2 = StringField('确认密码', validators=[DataRequired(message='确认密码必填'),
                                          Length(5, 10, message='账号长度只能在5到10位之间'),
                                          EqualTo('pw1', message='密码不一致')])
    icon = FileField('头像')


    # 定义validate_需校验的字段(self, field)
    def validate_username(self, field):
        # 校验User模型中的账号是否存在，如果存在抛异常
        user = User.query.filter(User.username == field.data).first()
        if user:
            raise ValidationError('注册账号已存在，请更换账号')
