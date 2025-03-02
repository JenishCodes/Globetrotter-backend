from app import db
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from app.jwt import generate_token


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(512), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.username}>"
    
    def get_user(user_id):
        return User.query.get(user_id)

    def get_username(username):
        return User.query.filter_by(username=username).first()

    def get_token(self):
        return generate_token(self.id)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
        }
