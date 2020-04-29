import flask
from flask import render_template

not_found_page = flask.Blueprint('not_found_page', __name__,
                                 template_folder='templates')


@not_found_page.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
