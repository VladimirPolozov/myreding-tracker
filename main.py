from flask import request
from flask_login import current_user
from pip._internal.vcs import git

from __init__ import *
# для создания сессии
from data import db_session
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
from blueprints.api import get_statics


@app.route('/update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/VladimirPolozov/myreding-tracker')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    # Создание БД
    db_session.global_init("db/tracker.sqlite")

    # Запуск приложения
    app.run(port=8080, host='127.0.0.1')
