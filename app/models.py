# from create_app import db
from flask_login import UserMixin
from app.utils import send_request
from app.config import settings


class User(UserMixin):
    def __init__(self, id: int, username: str, login: str, password: str):
        self.id = id
        self.username = username
        self.login = login
        self.password = password

    @staticmethod
    def get_user_by_id(id: int):
        response = send_request(settings.SERVER_URL + f'/api/v1/user/get_user?id={id}', "GET")
        return response

    @staticmethod
    def get_user_by_login(login: str):
        response = send_request(settings.SERVER_URL + f'/api/v1/user/get_user_by_login?login={login}', "GET")
        return response

    @staticmethod
    def add_user(data):
        response = send_request(settings.SERVER_URL + f'/api/v1/user/add_user', "POST", data)
        return response

    def __repr__(self):
        return '<User %r>' % self.username
