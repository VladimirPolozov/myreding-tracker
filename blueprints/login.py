import flask
from flask import url_for, render_template
from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.tables import User

login_form = flask.Blueprint('login_form', __name__,
                             template_folder='templates')


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_form.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # если пользователь авторизован
        return redirect(url_for('profile_page.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.name == form.username.data).first()
        if user and user.check_password(form.password.data,
                                        form.username.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("profile_page.profile"))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
