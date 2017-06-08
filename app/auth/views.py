from . import auth
from .forms import RegistrationForm
from ..models import User
from .. import db
from ..email import send_email
from flask import flash, redirect, url_for, render_template

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
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)