import flask
from flask_restful import abort
from data import db_session
from data.tables import Statics

get_statics_blue = flask.Blueprint('get_statics_blue', __name__,
                                   template_folder='templates')


@get_statics_blue.route('/api/<string:interval>')
def get_statics(interval):
    if interval != 'all' and \
            int(interval) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        return {'error': 'Not found'}
    session = db_session.create_session()
    statics = session.query(Statics).all()
    pages = 0
    time = 0
    for item in statics:
        if interval == '1' or interval == 'all':
            pages += int(item.january.split()[0])
            time += int(item.january.split()[1]) / 60
        if interval == '2' or interval == 'all':
            pages += int(item.february.split()[0])
            time += int(item.february.split()[1]) / 60
        if interval == '3' or interval == 'all':
            pages += int(item.march.split()[0])
            time += int(item.march.split()[1]) / 60
        if interval == '4' or interval == 'all':
            pages += int(item.april.split()[0])
            time += int(item.april.split()[1]) / 60
        if interval == '5' or interval == 'all':
            pages += int(item.may.split()[0])
            time += int(item.may.split()[1]) / 60
        if interval == '6' or interval == 'all':
            pages += int(item.june.split()[0])
            time += int(item.june.split()[1]) / 60
        if interval == '7' or interval == 'all':
            pages += int(item.july.split()[0])
            time += int(item.july.split()[1]) / 60
        if interval == '8' or interval == 'all':
            pages += int(item.august.split()[0])
            time += int(item.august.split()[1]) / 60
        if interval == '9' or interval == 'all':
            pages += int(item.september.split()[0])
            time += int(item.september.split()[1]) / 60
        if interval == '10' or interval == 'all':
            pages += int(item.october.split()[0])
            time += int(item.october.split()[1]) / 60
        if interval == '11' or interval == 'all':
            pages += int(item.november.split()[0])
            time += int(item.november.split()[1]) / 60
        if interval == '12' or interval == 'all':
            pages += int(item.december.split()[0])
            time += int(item.december.split()[1]) / 60

    if interval == 'all':
        time = round(time / 12 / len(statics), 1)
        pages = round(pages / 12 / len(statics), 1)
    else:
        time = round(time / len(statics), 1)
        pages = round(pages / len(statics), 1)
    try:
        speed = round(pages / time)
    except ZeroDivisionError:
        speed = 0

    return {'peopleCount': len(statics), 'data':
            [{'pages': pages, 'time': time, 'speed': speed}]}
