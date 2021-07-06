from models.models import User
from common.database import db_session


def save(user: User):
    db_session.add(user)
    db_session.commit()

    return user


def delete(user_id: int):
    User.query.filter_by(id=user_id).delete()
    db_session.commit()