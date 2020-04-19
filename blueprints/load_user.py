from data import db_session
from data.tables import User
from __init__ import login_manager


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)
