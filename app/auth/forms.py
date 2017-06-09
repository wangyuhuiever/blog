from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Regexp, Required

class RegistrationForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    username = StringField("用户名", validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字、下划线和小数点。')])
    password = PasswordField("密码", validators=[Required()])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo(
        'password','两次密码必须一致。')])
    submit = SubmitField("注册")

class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1,64), Email()])
    password = PasswordField("密码", validators=[Required()])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")