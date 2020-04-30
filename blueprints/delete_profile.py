import flask
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import User, Relationship, Statics

delete_profile = flask.Blueprint('delete_profile', __name__,
                                 template_folder='templates')


@delete_profile.route('/delete', methods=['GET', 'POST'])
def delete():
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    if request.method == "GET":
        return render_template("delete_profile.html")
    elif request.method == "POST":
        # просим подтвердить удаление профиля вводом пароля
        password = request.form.get('password')
        # если пароли не совпадают
        if not current_user.check_password(password, current_user.name):
            return render_template('delete_profile.html',
                                   message="Пароли не совпадают")
        # а если совпали
        session = db_session.create_session()
        # удаляем все связи этого пользователя с книгами
        session.query(Relationship).filter(
            Relationship.user_id == current_user.id).delete()
        # и его статистику
        session.query(Statics).filter(
            Statics.user_id == current_user.id).delete()
        # удаляем самого пользователя
        session.query(User).filter(User.id == current_user.id).delete()
        session.commit()
        # сообщаем пользователю, что мы удалили его профиль
        return render_template('profile_is_delete.html')
