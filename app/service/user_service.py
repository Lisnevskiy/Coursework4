import base64
import hashlib
import hmac

from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from app.dao.user_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, data):
        data['password'] = self.make_user_password_hash(data['password'])


        return self.dao.create(data)

    def update(self, uid, data):
        user = self.get_one(uid)
        data['password'] = self.make_user_password_hash(data['password'])

        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.dao.update(user)

    def update_partial(self, uid, data):
        user = self.get_one(uid)
        data['password'] = self.make_user_password_hash(data['password'])

        if 'username' in data:
            user.username = data.get("username")
        if 'password' in data:
            user.password = data.get("password")
        if 'role' in data:
            user.role = data.get("role")

        self.dao.update(user)

    def delete(self, uid):
        self.dao.delete(uid)

    def make_user_password_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256', other_password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        )
