from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import Length, Required, Email, Regexp, ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class EditProfileForm(FlaskForm):
    name = StringField("姓名", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0,64)])
    about_me = TextAreaField("自我介绍")
    submit = SubmitField("确认")

class EditProfileAdminForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    username = StringField("用户名", validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                          '用户名只能包含字母，数字，下划线和小数点。')])
    confirmed = BooleanField("验证信息")
    role = SelectField("角色", coerce=int)
    name = StringField("姓名", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0, 64)])
    about_me = TextAreaField("自我介绍")
    submit = SubmitField("确认")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")

class PostForm(FlaskForm):
    body = PageDownField("写点什么吧...", validators=[Required()])
    submit = SubmitField("确认")

class CommentForm(FlaskForm):
    body = StringField('', validators=[Required()])
    submit = SubmitField("提交")