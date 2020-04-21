from datetime import datetime
import flask
import pytz
import requests
from flask import url_for, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Book, Relationship

my_book_page = flask.Blueprint('my_book_page', __name__,
                               template_folder='templates')


@my_book_page.route('/mybook/<int:book_id>', methods=['POST', 'GET'])
def my_book(book_id):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    elif request.method == "GET":
        book = {}

        session = db_session.create_session()
        book_data = session.query(Relationship).filter(
            Relationship.user_id == current_user.id,
            Relationship.book_id == book_id).first()
        book['id'] = str(book_id)
        book['pageCount'] = book_data.pages
        book['page_read'] = book_data.pages_read
        try:
            hours = str(book_data.time // 60)
            if len(hours) == 1:
                hours = '0' + hours
            minute = str(book_data.time % 60)
            if len(minute) == 1:
                minute = '0' + minute
            book['time'] = hours + ':' + minute
            book['speed'] = book['page_read'] // (book_data.time / 60)
            book['percent'] = book['page_read'] // (book['pageCount'] / 100)
        except Exception:
            book['page_read'] = 0
            book['time'] = "00:00"
            book['speed'] = 0
            book['percent'] = 0

        if book['percent'] == 100:
            book['status'] = 'Прочитал!'
        elif book['page_read'] > 0:
            book['status'] = 'Читаю'
        else:
            book['status'] = 'Хочу прочитать'

        book_data = session.query(Book).filter(Book.id == book_id).first()
        response = requests.get(book_data.link).json()

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
        if request.form.get('time') == '00:00':
            return "<h1>Значение '00:00' у подя 'время' - недопустимо</h><br>" +\
                   "<a href=\'/mybook/" + str(book_id) + "\'>OK</a>"

        pages_read = request.form.get('pages_read')
        time = request.form.get('time').split(':')
        time = int(time[0] * 60) + int(time[1])

        session = db_session.create_session()
        relation = session.query(Relationship).filter(
            Relationship.user_id == current_user.id,
            Relationship.book_id == book_id).first()
        relation.pages_read = relation.pages_read + int(pages_read)
        relation.time = time + relation.time
        relation.last_activity = datetime.now(pytz.timezone('Europe/Moscow'))
        session.commit()

        return "<h1>Активность добавлена</h1><br>" +\
               "<a href=\'/mybook/" + str(book_id) + "\'>OK</a>"
