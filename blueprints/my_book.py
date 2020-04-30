from datetime import datetime
import flask
import requests
from flask import url_for, request, render_template
from flask_login import current_user
from flask_restful import abort
from werkzeug.utils import redirect
from data import db_session
from data.tables import Book, Relationship, Statics

my_book_page = flask.Blueprint('my_book_page', __name__,
                               template_folder='templates')


@my_book_page.route('/mybook/<int:book_id>', methods=['POST', 'GET'])
def my_book(book_id):
    """Данные о книге, добавленной пользователем"""
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    elif request.method == "GET":
        try:
            book = {}

            session = db_session.create_session()
            book_data = session.query(Relationship).filter(
                Relationship.user_id == current_user.id,
                Relationship.book_id == book_id).first()
            book['id'] = str(book_id)
            book['pageCount'] = book_data.pages
            book['page_read'] = book_data.pages_read
            # перевод времени из минут в чч:мм
            # и вычисление скорости, если это возможно
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
            #  противном случае принимаем все значения за ноль
            except Exception:
                book['page_read'] = 0
                book['time'] = "00:00"
                book['speed'] = 0
                book['percent'] = 0

            # если пользователь прочитал книгу
            if book['percent'] == 100:
                book['status'] = 'Прочитал!'
            # начал читать
            elif book['page_read'] > 0:
                book['status'] = 'Читаю'
            # не начал
            else:
                book['status'] = 'Хочу прочитать'

            # находим книгу в таблице книг по её id
            book_data = session.query(Book).filter(Book.id == book_id).first()
            # запрос в Google Api Books
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
        except Exception as e:  # если что-то идёт не так
            print(e)
            abort(404)

    # когда пользователь добавляет активность
    elif request.method == "POST":
        if request.form.get('time') == '00:00':
            return redirect(
                url_for(
                    'books_page.books',
                    message="Значение '00:00' у поля 'время' недопустимо"))

        # добавляем полученные данные
        # предварительно обработав их
        pages_read = request.form.get('pages_read')
        time = request.form.get('time').split(':')
        time = int(int(time[0]) * 60) + int(time[1])

        session = db_session.create_session()
        relation = session.query(Relationship).filter(
            Relationship.user_id == current_user.id,
            Relationship.book_id == book_id).first()
        relation.pages_read = relation.pages_read + int(pages_read)
        relation.time = time + relation.time
        relation.last_activity =\
            str(datetime.now().year) + '-' + str(datetime.now().month)
        session.commit()

        # добавляем статистику в соответствующий месяц
        sctatic = session.query(Statics).filter(
            Statics.user_id == current_user.id).first()
        if datetime.now().month == 1:
            sctatic.january = \
                str(int(sctatic.january.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.january.split()[1]) + time)
        elif datetime.now().month == 2:
            sctatic.february = \
                str(int(sctatic.february.split()[0]) + int(pages_read)) + ' ' \
                + str(int(sctatic.february.split()[1]) + time)
        elif datetime.now().month == 3:
            sctatic.march = \
                str(int(sctatic.march.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.march.split()[1]) + time)
        elif datetime.now().month == 4:
            sctatic.april = \
                str(int(sctatic.april.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.april.split()[1]) + time)
        elif datetime.now().month == 5:
            sctatic.may = \
                str(int(sctatic.may.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.may.split()[1]) + time)
        elif datetime.now().month == 6:
            sctatic.june = \
                str(int(sctatic.june.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.june.split()[1]) + time)
        elif datetime.now().month == 7:
            sctatic.july = \
                str(int(sctatic.july.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.july.split()[1]) + time)
        elif datetime.now().month == 8:
            sctatic.august = \
                str(int(sctatic.august.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.august.split()[1]) + time)
        elif datetime.now().month == 9:
            sctatic.september = \
                str(int(sctatic.september.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.september.split()[1]) + time)
        elif datetime.now().month == 10:
            sctatic.october = \
                str(int(sctatic.october.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.october.split()[1]) + time)
        elif datetime.now().month == 11:
            sctatic.november = \
                str(int(sctatic.november.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.november.split()[1]) + time)
        elif datetime.now().month == 12:
            sctatic.december = \
                str(int(sctatic.december.split()[0]) + int(pages_read)) + \
                ' ' + str(int(sctatic.december.split()[1]) + time)
        session.commit()

        return redirect(url_for('books_page.books',
                                message='Активность добавлена'))


@my_book_page.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
