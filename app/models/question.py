from app import db
from datetime import datetime, timezone


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    destination_id = db.Column(
        db.Integer, db.ForeignKey("destinations.id"), nullable=False
    )
    hint_taken = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)
    option_selected = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Question {self.id}>"

    def get_question(question_id):
        return Question.query.filter_by(id=question_id).first()

    def get_unanswered_question(user_id):
        return Question.query.filter_by(user_id=user_id, option_selected=None).first()

    def get_user_score(user_id):
        return db.session.query(db.func.sum(Question.points)).filter(
            Question.user_id == user_id,
            Question.option_selected != None,
        ).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hint_taken": self.hint_taken,
            "option_selected": self.option_selected,
            "points": self.points,
            "created_at": self.created_at,
        }
