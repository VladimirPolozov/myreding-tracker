import flask
from flask import request, render_template, url_for
from werkzeug.utils import redirect
from data import db_session
from data.tables import User

recovery_form = flask.Blueprint('recovery_form', __name__,
                                template_folder='templates')
# Словарь для восстановления пароля
DATA = {'index_recovery': 0}


@recovery_form.route('/recovery', methods=['POST', 'GET'])
def recovery():
    global DATA
    if request.method == 'GET':
        return render_template('recovery.html',
                               form_text="Введите имя пользователя",
                               hint="Имя",
                               button_text="Дальше")
    elif request.method == 'POST':
        if DATA['index_recovery'] == 0:
            name = request.form.get('form').strip()
            session = db_session.create_session()
            user = session.query(User).filter(User.name == name).first()
            if not user:
                return render_template(
                    'recovery.html', form_text="Введите имя пользователя",
                    hint="Имя", button_text="Дальше",
                    message="Такое имя пользователя не найдено")
            DATA['index_recovery'] = 1
            DATA['user'] = user
            return render_template('recovery.html',
                                   form_text=user.question,
                                   hint="Ответ",
                                   button_text="Ответить")
        elif DATA['index_recovery'] == 1:
            answer = request.form.get('form').strip()
            if not DATA['user'].check_answer(answer, DATA['user'].name):
                return render_template('recovery.html',
                                       form_text=DATA['user'].question,
                                       hint="Ответ",
                                       button_text="Ответить",
                                       message="Неверный ответ")
            DATA['index_recovery'] = 2
            return render_template('recovery.html',
                                   is_password=True)
        elif DATA['index_recovery'] == 2:
            password = request.form.get('password')
            password2 = request.form.get('password2')
            if password != password2:
                return render_template('recovery.html',
                                       is_password=False,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            DATA['user'].password = DATA['user'].set_password(password)
            session.commit()
            DATA['index_recovery'] = 0
            DATA['user'] = 0
            return redirect(url_for('login_form.login'))
