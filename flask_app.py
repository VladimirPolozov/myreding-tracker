from flask import request
from flask_login import current_user

from __init__ import *
# для создания сессии
from data import db_session
# импрот функций-страниц
from blueprints.delete_profile import delete
from blueprints.load_user import load_user
from blueprints.login import login
from blueprints.logout import logout
from blueprints.register import register
from blueprints.statics import statics
from blueprints.books import books
from blueprints.profile import profile
from blueprints.add_book import add_book
from blueprints.book import book
from blueprints.delete_book import delete_book
from blueprints.api import get_statics


# Создание БД
db_session.global_init("db/tracker.sqlite")
if __name__ == '__main__':
    # Запуск приложения
    app.run(port=8080, host='127.0.0.1')
