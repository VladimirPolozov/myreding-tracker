import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db_session
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import datetime


class User(SqlAlchemyBase, UserMixin):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)  # Уникальный id пользователя
    name = sqlalchemy.Column(sqlalchemy.String,
                             unique=True,
                             index=True)  # Уникальное имя пользователя
    password = sqlalchemy.Column(sqlalchemy.String)  # хэшированный пароль
    # Секретный пароль, на случай, если пользователь забудет пароль
    question = sqlalchemy.Column(sqlalchemy.String)
    # Ответ на секретный вопрос
    answer = sqlalchemy.Column(sqlalchemy.String)

    # Это позваолит получить все книги пользователя
    relationship = orm.relation("Relationship", back_populates='user')

    def set_password(self, password):
        """Хэширование пароля"""
        return generate_password_hash(password)

    def check_password(self, password, username):
        """Проверка введёного пароля"""
        session = db_session.create_session()
        # Находим пользователя по имени
        user = session.query(User).filter(User.name == username).first()
        # Проверка, совпадает ли введёный пользователем пароль
        # с рахэшированным паролем из БД
        return check_password_hash(user.password, password)

    def check_answer(self, answer, username):
        """Проверка введёного секретного ответа на секретный вопрос
           Логика работы анологична check_password, но вместо
           password - answer"""
        session = db_session.create_session()
        user = session.query(User).filter(User.name == username).first()
        return check_password_hash(user.answer, answer)


class Relationship(SqlAlchemyBase):
    """Таблица отношений пользователь к книгам"""
    __tablename__ = 'relationship'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # id пользователя, который добавил книгу с id book_id к себе на полку
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    # id книги, которую пользователь с id user_id добавил к себе на полку
    book_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id"))
    # кол-во страниц в книге по мнению пользователя
    pages = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # кол-во прочитанных страниц книги
    pages_read = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # кол-во сумморного времени затраченного на чтение
    time = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # месяц и год последней активности
    last_activity = sqlalchemy.Column(
        sqlalchemy.String,
        default=str(datetime.now().year) + '-' + str(datetime.now().month))

    user = orm.relation('User')
    book = orm.relation('Book')


class Book(SqlAlchemyBase):
    """Таблица с книгами"""
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)  # id книги
    # ссылка запроса для данной книги, в Google Api Books
    link = sqlalchemy.Column(sqlalchemy.String,
                             index=True)


class Statics(SqlAlchemyBase, SerializerMixin):
    """Таблица со статистикой пользователя по месяцам"""
    __tablename__ = 'statics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    january = sqlalchemy.Column(sqlalchemy.String,
                                default='0 0')
    february = sqlalchemy.Column(sqlalchemy.String,
                                 default='0 0')
    march = sqlalchemy.Column(sqlalchemy.String,
                              default='0 0')
    april = sqlalchemy.Column(sqlalchemy.String,
                              default='0 0')
    may = sqlalchemy.Column(sqlalchemy.String,
                            default='0 0')
    june = sqlalchemy.Column(sqlalchemy.String,
                             default='0 0')
    july = sqlalchemy.Column(sqlalchemy.String,
                             default='0 0')
    august = sqlalchemy.Column(sqlalchemy.String,
                               default='0 0')
    september = sqlalchemy.Column(sqlalchemy.String,
                                  default='0 0')
    october = sqlalchemy.Column(sqlalchemy.String,
                                default='0 0')
    november = sqlalchemy.Column(sqlalchemy.String,
                                 default='0 0')
    december = sqlalchemy.Column(sqlalchemy.String,
                                 default='0 0')

    user = orm.relation('User')
