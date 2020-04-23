from flask import Flask
from flask_login import LoginManager
# Импорт чертежей
from flask_restful import Api

from blueprints.delete_profile import delete_profile
from blueprints.logout import blue_logout
from blueprints.register import registration_form
from blueprints.login import login_form
from blueprints.unauthorized import unauthorized_form
from blueprints.recovery import recovery_form
from blueprints.main_page import main_page
from blueprints.statics import statics_page
from blueprints.books import books_page
from blueprints.profile import profile_page
from blueprints.add_book import add_book_page
from blueprints.book import book_page
from blueprints.my_book import my_book_page
from blueprints.delete_book import delete_book_page
from blueprints.api import api_blue

# Создание приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'p996O41lOv31O'
# Api нашего приложения
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
# регистрация чертежей
app.register_blueprint(delete_profile)
app.register_blueprint(blue_logout)
app.register_blueprint(registration_form)
app.register_blueprint(login_form)
app.register_blueprint(unauthorized_form)
app.register_blueprint(recovery_form)
app.register_blueprint(main_page)
app.register_blueprint(statics_page)
app.register_blueprint(books_page)
app.register_blueprint(profile_page)
app.register_blueprint(add_book_page)
app.register_blueprint(book_page)
app.register_blueprint(my_book_page)
app.register_blueprint(delete_book_page)
app.register_blueprint(api_blue)
# Ключ для взаимодействия с Google Api Books
KEY = "key=AIzaSyDjcLFRSlro98kWymIkyX21yj8h4FGPFfc"
