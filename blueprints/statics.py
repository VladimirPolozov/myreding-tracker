import flask
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from data import db_session
from data.tables import Statics

statics_page = flask.Blueprint('statics_page', __name__,
                               template_folder='templates')


@statics_page.route('/statics/<view>')
def statics(view):
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    title = 'Статистика'
    active = 'static'
    labels = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    values = []
    if view == 'pages':
        legend = 'Страниц прочитано'
        session = db_session.create_session()
        static = session.query(Statics).filter(
            Statics.user_id == current_user.id).one()
        values.append(int(static.january.split()[0]))
        values.append(int(static.february.split()[0]))
        values.append(int(static.march.split()[0]))
        values.append(int(static.april.split()[0]))
        values.append(int(static.may.split()[0]))
        values.append(int(static.june.split()[0]))
        values.append(int(static.july.split()[0]))
        values.append(int(static.august.split()[0]))
        values.append(int(static.september.split()[0]))
        values.append(int(static.october.split()[0]))
        values.append(int(static.november.split()[0]))
        values.append(int(static.december.split()[0]))
    elif view == 'time':
        legend = 'Время за чтением (в минутах)'
        session = db_session.create_session()
        static = session.query(Statics).filter(
            Statics.user_id == current_user.id).one()
        values.append(int(static.january.split()[1]))
        values.append(int(static.february.split()[1]))
        values.append(int(static.march.split()[1]))
        values.append(int(static.april.split()[1]))
        values.append(int(static.may.split()[1]))
        values.append(int(static.june.split()[1]))
        values.append(int(static.july.split()[1]))
        values.append(int(static.august.split()[1]))
        values.append(int(static.september.split()[1]))
        values.append(int(static.october.split()[1]))
        values.append(int(static.november.split()[1]))
        values.append(int(static.december.split()[1]))
    elif view == 'speed':
        legend = 'Скорость стр/мин'
        session = db_session.create_session()
        static = session.query(Statics).filter(
            Statics.user_id == current_user.id).one()
        try:
            values.append(
                int(static.january.split()[0]) / int(static.january.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.february.split()[0]) / int(static.february.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.march.split()[0]) / int(static.march.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.april.split()[0]) / int(static.april.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.may.split()[0]) / int(static.may.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.june.split()[0]) / int(static.june.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.july.split()[0]) / int(static.july.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.august.split()[0]) / int(static.august.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.september.split()[0]) / int(static.september.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.october.split()[0]) / int(static.october.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.november.split()[0]) / int(static.november.split()[1]))
        except ZeroDivisionError:
            values.append(0)
        try:
            values.append(
                int(static.december.split()[0]) / int(static.december.split()[1]))
        except ZeroDivisionError:
            values.append(0)
    return render_template('static.html',
                           title=title,
                           active=active,
                           values=values,
                           labels=labels,
                           legend=legend)
