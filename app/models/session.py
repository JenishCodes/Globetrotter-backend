from app import db
from datetime import datetime, timezone

from sqlalchemy import text



class Session(db.Model):
    __tablename__ = "sessions"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    current_question = db.Column(db.Integer, default=1)
    completed_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def find_session(session_id):
        return Session.query.filter_by(id=session_id).first()
    
    def find_ongoing_session(user_id):
        return Session.query.filter_by(user_id=user_id, completed_at=None).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "current_question":self.current_question,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
        }


class SessionQuestion(db.Model):
    __tablename__ = "session_questions"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    order =  db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def find_session_question(question_ord_id, session_id):
        return db.session.execute(text(f"SELECT q.* FROM session_questions as sq inner join questions as q on q.id = sq.question_id Where sq.session_id = {session_id} and sq.order= {question_ord_id}")).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "order": self.order,
            "created_at": self.created_at,
        }