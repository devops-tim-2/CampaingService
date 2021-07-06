from models.models import User
from repository import user_repository


def add(user: dict):
    user = User(id=user['id'])

    user = user_repository.save(user)

    return user


def delete(user_id: int):
    user_repository.delete(user_id)

    return True
