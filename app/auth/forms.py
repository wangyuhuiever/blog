from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Regexp, Required
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    username = StringField("用户名", validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字、下划线和小数点。')])
    password = PasswordField("密码", validators=[Required()])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo(
        'password','两次密码必须一致。')])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1,64), Email()])
    password = PasswordField("密码", validators=[Required()])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("原密码", validators=[Required()])
    new_password = PasswordField("新密码", validators=[Required()])
    new_password2 = PasswordField("确认新密码", validators=[Required(), EqualTo("new_password",
                                                                           "两次密码必须一致")])
    submit = SubmitField("确认修改")

class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[Required()])
    submit = SubmitField('确认修改')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

class PasswordResetRequestForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('确认')

class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[Required()])
    password2 = PasswordField("确认密码", validators=[
        Required(), EqualTo('password', "两次密码必须一致")])
    submit = SubmitField("确认")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError("当前邮箱未注册")