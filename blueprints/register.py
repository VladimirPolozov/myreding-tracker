import flask
from flask import url_for, render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from data import db_session
from data.tables import User, Statics

registration_form = flask.Blueprint('registration_form', __name__,
                                    template_folder='templates')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')])
    question = StringField(
        'Секретный вопрос (например: \"Любимая музыкальная группа?\")',
        validators=[DataRequired()])
    answer = StringField(
        'Ответ на секретный вопрос (например: \"for KING & COUNTRY\")',
        validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        session = db_session.create_session()
        user = session.query(User).filter(User.name == username.data).first()
        if user is not None:
            raise ValidationError('Такое имя пользователя уже существует!')


@registration_form.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:  # если пользователь авторизован
        return redirect(url_for('profile_page.profile'))
    if form.validate_on_submit():
        session = db_session.create_session()

        user = User()
        user.name = form.username.data
        if form.question.data[-1] != '?':
            form.question.data += '?'
        user.question = form.question.data
        user.answer = user.set_password(form.answer.data)
        user.password = user.set_password(form.password.data)
        session.add(user)
        session.commit()

        statics = Statics()
        statics.user_id = user.id
        session.add(statics)
        session.commit()

        return redirect(url_for('login_form.login'))
    return render_template('register.html', form=form)
