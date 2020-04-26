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
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        grequest = "https://www.googleapis.com/books/v1/volumes?" + KEY + '&q='
        if title:
            grequest += "intitle:" + title.rstrip()
        if author:
            grequest += "inauthor:" + author.rstrip()
        response = requests.get(grequest)
        response = response.json()
        books = []
        if 'error' not in response and response['totalItems'] != 0:
            for item in response['items']:

                session = db_session.create_session()
                book = session.query(Book).filter(
                    Book.link == item['selfLink']).first()

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
            if not books:
                books.append(None)
            return render_template('add_book.html', books=books)
        return render_template('add_book.html', books=[None])
    return render_template('add_book.html', books=False)
