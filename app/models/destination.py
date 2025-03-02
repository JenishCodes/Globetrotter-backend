from app import db


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(512), unique=True, nullable=False)
    country = db.Column(db.String(1024), nullable=False)
    clue_1 = db.Column(db.String(1024), nullable=False)
    clue_2 = db.Column(db.String(1024), nullable=False)
    fun_fact_1 = db.Column(db.String(1024), nullable=False)
    fun_fact_2 = db.Column(db.String(1024), nullable=False)
    trivia_1 = db.Column(db.String(1024), nullable=False)
    trivia_2 = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f"<City {self.city}>"

    def get_destination(destination_id):
        return Destination.query.filter_by(id=destination_id).first()

    def get_random_destinations(destination_id=None, limit=1):
        return (
            Destination.query.filter(Destination.id != destination_id)
            .order_by(db.func.random())
            .limit(limit)
            .all()
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "country": self.country,
            "clue_1": self.clue_1,
            "clue_2": self.clue_2,
            "fun_fact_1": self.fun_fact_1,
            "fun_fact_2": self.fun_fact_2,
            "trivia_1": self.trivia_1,
            "trivia_2": self.trivia_2,
        }
