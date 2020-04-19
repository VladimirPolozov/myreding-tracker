import flask
from flask import url_for
from flask_login import logout_user, current_user
from werkzeug.utils import redirect

blue_logout = flask.Blueprint('blue_logout', __name__,
                              template_folder='templates')


@blue_logout.route('/logout')
def logout():
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    logout_user()
    return redirect(url_for('unauthorized_form.unauthorized'))
