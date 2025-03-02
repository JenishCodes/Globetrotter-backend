from app import db
from datetime import datetime, timezone

import uuid
import secrets


class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    uri = db.Column(db.String(512), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Link of user {self.user_id}>"

    def get_user_link(user_id):
        return Link.query.filter_by(user_id=user_id).first()

    def get_uri_link(uri):
        return Link.query.filter_by(uri=uri).first()

    def generate_uri():
        return f"{uuid.uuid4()}-{secrets.token_urlsafe(8)}"

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "uri": self.uri,
            "created_at": self.created_at,
        }
