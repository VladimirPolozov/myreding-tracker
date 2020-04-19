import flask
import requests
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Book, Relationship

book_page = flask.Blueprint('book_page', __name__,
                            template_folder='templates')


@book_page.route('/book/<path:selfLink>', methods=['POST', 'GET'])
def book(selfLink):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    elif request.method == "GET":
        response = requests.get(selfLink)
        response = response.json()
        book = {}
        try:
            book['title'] = response['volumeInfo']['title']
        except KeyError:
            book['title'] = "Без названия"
        try:
            book['authors'] = response['volumeInfo']['authors']
        except KeyError:
            book['authors'] = "Автор не указан"
        try:
            book['description'] = response['volumeInfo']['description']
        except KeyError:
            book['description'] = "Описание отсутствует"
        try:
            book['image'] = response['volumeInfo']['imageLinks'][
                'thumbnail']
        except KeyError:
            book['link'] = 'static/img/nothing.jpg'
        try:
            book['pageCount'] = response['volumeInfo']['pageCount']
        except KeyError:
            book['pageCount'] = 1

        book['isAvailableEpub'] = True
        book['isAvailablePdf'] = True
        try:
            book['epub'] = response['accessInfo']['epub']['acsTokenLink']
        except KeyError:
            book['isAvailableEpub'] = False
        try:
            book['pdf'] = response['accessInfo']['pdf']['acsTokenLink']
        except KeyError:
            book['isAvailablePdf'] = False
        book['selfLink'] = response['selfLink']
        book['link'] = response['volumeInfo']['canonicalVolumeLink']
        book['webReaderLink'] = response['accessInfo']['webReaderLink']

        return render_template('book.html', book=book)
    elif request.method == 'POST':
        session = db_session.create_session()

        book = Book()
        book.link = selfLink
        session.add(book)
        session.commit()

        relation = Relationship()
        relation.user_id = current_user.id
        relation.book_id = book.id
        relation.pages = int(request.form.get('pages'))
        session.add(relation)
        session.commit()

        return render_template('book_is_added.html', book=book)