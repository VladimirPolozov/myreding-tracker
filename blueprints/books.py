import flask
import requests
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Relationship, Book

books_page = flask.Blueprint('books_page', __name__,
                             template_folder='templates')


@books_page.route(
    '/books/', defaults={'message': ''}, methods=['GET', 'POST'])
@books_page.route('/books/<message>', methods=['GET', 'POST'])
def books(message):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    if message in ['Активность добавлена',
                   "Значение '00:00' у поля 'время' недопустимо"]:
        message = message
    else:
        message = ''
    title = 'Полка'
    active = 'books'
    session = db_session.create_session()
    # находим все книги пользователя по его id
    user_books = session.query(Relationship).filter(
        Relationship.user_id == current_user.id).all()
    books = []
    for item in user_books:
        book_data = session.query(Book).filter(Book.id == item.book_id).first()
        item = requests.get(book_data.link).json()

        book = {}
        book['id'] = str(book_data.id)
        book['selfLink'] = item['selfLink']
        try:
            book['title'] = item['volumeInfo']['title']
        except KeyError:
            book['title'] = "Без названия"
        try:
            book['authors'] = item['volumeInfo']['authors']
        except KeyError:
            book['authors'] = ["Автор не указан"]
        try:
            book['image'] = item['volumeInfo']['imageLinks'][
                'thumbnail']
        except KeyError:
            book['image'] = 'static/img/nothing.jpg'
        books.append(book)
    return render_template('books.html',
                           title=title,
                           active=active,
                           books=books,
                           message=message)
