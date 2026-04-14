from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)

    def __init__(self, name):
        self.name = name.lower().strip()

    def __repr__(self):
        return f"<Skill {self.name}>"