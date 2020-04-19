import flask
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

profile_page = flask.Blueprint('profile_page', __name__,
                               template_folder='templates')


@profile_page.route('/profile')
def profile():
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    title = 'Профиль'
    active = 'profile'
    return render_template('profile.html', title=title, active=active)
