import flask

delete_book_page = flask.Blueprint('delete_book_page', __name__,
                               template_folder='templates')


@delete_book_page.route('/delete_book/<path:selfLink>', methods=['POST', 'GET'])
def delete_book(selfLink):
    pass