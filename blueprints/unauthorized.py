import flask
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

unauthorized_form = flask.Blueprint('unauthorized_form', __name__,
                                    template_folder='templates')


@unauthorized_form.route('/unauthorized')
def unauthorized():
    """Страница заглушка для не авторизованных пользователей"""
    if current_user.is_authenticated:  # если пользователь авторизован
        return redirect(url_for('profile_page.profile'))
    return render_template("unauthorized.html")
