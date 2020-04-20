import flask
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Relationship

delete_book_page = flask.Blueprint('delete_book_page', __name__,
                                   template_folder='templates')


@delete_book_page.route('/delete_book/<path:book_id>', methods=['POST', 'GET'])
def delete_book(book_id):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    elif request.method == "GET":
        return render_template('delete_book.html')
    elif request.method == "POST":
        password = request.form.get('password')
        # если пароли не совпадают
        if not current_user.check_password(password, current_user.name):
            return render_template('delete_profile.html',
                                   message="Пароли не совпадают")
        # а если совпали
        session = db_session.create_session()
        # удаляем книгу
        session.query(Relationship).filter(
            Relationship.user_id == current_user.id,
            Relationship.book_id == book_id).delete()
        session.commit()
        # сообщаем пользователю, что мы удалили его книгу
        return render_template('book_is_delete.html')
