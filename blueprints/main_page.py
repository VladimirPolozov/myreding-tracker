import flask
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

main_page = flask.Blueprint('main_page', __name__,
                            template_folder='templates')


@main_page.route('/')
@main_page.route('/main')
def main():
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    username = current_user.name
    title = 'Главная'
    active = 'main'
    return render_template("main.html", title=title, active=active,
                           username=username)
