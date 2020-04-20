import flask
import requests
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Book, Relationship

my_book_page = flask.Blueprint('my_book_page', __name__,
                               template_folder='templates')


@my_book_page.route('/mybook/<path:selfLink>', methods=['POST', 'GET'])
def my_book(selfLink):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    elif request.method == "GET":
        book = {}

        session = db_session.create_session()
        book_data = session.query(Book).filter(Book.link == selfLink).first()
        book_data = session.query(Relationship).filter(
            Relationship.book_id == book_data.id,
            Relationship.user_id == current_user.id).first()
        book['pageCount'] = book_data.pages
        response = requests.get(selfLink)
        response = response.json()

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

        return render_template('my_book.html', book=book)

    elif request.method == "POST":
        pages_read = request.form.get('pages_read')
        time = request.form.get('time').split(':')
        time = int(time[0] * 60) + int(time[1])

        session = db_session.create_session()
        book = session.query(Book).filter(Book.link == selfLink).first()
        relation = session.query(Relationship).filter(
            Relationship.user_id == current_user.id,
            Relationship.book_id == book.id).first()
        relation.pages_read = pages_read
        time += relation.time
        relation.time = time
        session.commit()

        return "<h1>Активность добавлена</h1><br>" + "<a href=\'/mybook/" +\
               selfLink + "\'>Ок</a>"
