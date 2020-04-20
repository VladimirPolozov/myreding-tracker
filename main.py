import requests
from data.tables import *
from flask_login import current_user
# импорт приложения
from __init__ import *
# импрот функций-страниц
from blueprints.delete_profile import delete
from blueprints.load_user import load_user
from blueprints.login import login
from blueprints.logout import logout
from blueprints.register import register
from blueprints.main_page import main
from blueprints.statics import statics
from blueprints.books import books
from blueprints.profile import profile
from blueprints.add_book import add_book
from blueprints.book import book
from blueprints.delete_book import delete_book


if __name__ == '__main__':
    # Создание БД
    db_session.global_init("db/tracker.sqlite")

    # Запуск приложения
    app.run(port=8080, host='127.0.0.1')
