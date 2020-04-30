import flask
import requests
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Book, Relationship

# Ключ для взаимодействия с Google Api Books
KEY = "key=AIzaSyDjcLFRSlro98kWymIkyX21yj8h4FGPFfc"
add_book_page = flask.Blueprint('add_book_page', __name__,
                                template_folder='templates')


@add_book_page.route('/add_book', methods=['POST', 'GET'])
def add_book():
    """Добавление книги"""
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    if request.method == 'POST':
        # передача в переменную данных из поля 'название книрги'
        title = request.form.get('title')
        # передача в переменную данных из поля 'автор книрги'
        author = request.form.get('author')
        # шаблон запроса в Google Ap Books
        grequest = "https://www.googleapis.com/books/v1/volumes?" + KEY + '&q='
        if title:  # если поле не пустое
            grequest += "intitle:" + title.rstrip()
        if author:  # аналогично
            grequest += "inauthor:" + author.rstrip()
        # запрос
        response = requests.get(grequest)
        # перевод запрос в json
        response = response.json()
        books = []
        # если в запросе нет ошибки
        if 'error' not in response:
            # проходим по полученным книгам
            for item in response['items']:
                # проверка есть ли уже книга в БД
                session = db_session.create_session()
                book = session.query(Book).filter(
                    Book.link == item['selfLink']).first()
                # если есть, пропускаем её
                if book and session.query(Relationship).filter(
                        Relationship.book_id == book.id,
                        Relationship.user_id == current_user.id).first():
                    continue

                book = {}
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
                    book['description'] = item['volumeInfo']['description']
                except KeyError:
                    book['description'] = "Описание отсутствует"
                try:
                    book['image'] = item['volumeInfo']['imageLinks'][
                        'thumbnail']
                except KeyError:
                    book['image'] = 'static/img/nothing.jpg'
                books.append(book)
            # если не оказалось подходяших книг
            if not books:
                books.append(None)
            return render_template('add_book.html', books=books)
        return render_template('add_book.html', books=[None])
    return render_template('add_book.html', books=False)
