#! -*- encoding:utf-8 -*-
from . import auth
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, ChangeEmailForm, PasswordResetRequestForm, \
    PasswordResetForm
from ..models import User
from .. import db
from ..email import send_email
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user, login_user, logout_user

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user, "验证邮箱", 'auth/email/confirm',
                   user=user, token=token)
        flash("一封邮件已经发往您的邮箱")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('验证通过')
        return redirect(url_for('main.index'))
    else:
        flash('验证信息有误')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "验证邮箱", 'auth/email/confirm',
               user=current_user, token=token)
    flash('一封新的邮件已经发往您的邮箱')
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("用户名或密码错误")
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出了登录')
    return redirect(url_for('auth.login'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash("密码修改成功")
            return redirect(url_for('main.index'))
        else:
            flash("原密码错误")
    return render_template('auth/change_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, "验证新邮箱", 'auth/email/change_email',
                       user=current_user, token=token)
            flash("一封邮件已经发往您的邮箱")
            return redirect(url_for('main.index'))
        else:
            flash("密码错误")
    return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('邮箱地址已变更')
    else:
        flash('变更失败')
    return redirect(url_for('main.index'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, "重置密码", 'auth/email/reset_password',
                       user=user, token=token)
            flash("一封邮件已经发送到您的邮箱")
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form =PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('密码重置成功')
            return redirect(url_for('main.index'))
        else:
            flash('请检查链接是否错误')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
