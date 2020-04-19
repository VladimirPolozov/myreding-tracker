import flask
from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

statics_page = flask.Blueprint('statics_page', __name__,
                               template_folder='templates')


@statics_page.route('/statics')
def statics():
    if not current_user.is_authenticated:  # если пользователь не авторизован
        return redirect(url_for('unauthorized_form.unauthorized'))
    title = 'Статистика'
    active = 'static'
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    values = [10, 9, 8, 7, 6, 4, 7, 8, 12, 10, 9, 9]
    return render_template('static.html',
                           title=title,
                           active=active,
                           values=values,
                           labels=labels,
                           legend=legend)
