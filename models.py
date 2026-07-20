from datetime import datetime
from flask_login import UserMixin

from extensions import db
from datetime import datetime, timedelta


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.utcnow() + timedelta(hours=5, minutes=30)
)

    # One-to-One Relationship
    profile = db.relationship(
        "UserProfile",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    dob = db.Column(db.Date)

    gender = db.Column(db.String(20))

    height = db.Column(db.Float)

    weight = db.Column(db.Float)

    blood_group = db.Column(db.String(10))

    existing_disease = db.Column(db.Text)

    allergies = db.Column(db.Text)

    current_medications = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<UserProfile {self.user_id}>"
    




class Consultation(db.Model):
    __tablename__ = "consultations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(255), nullable=False)

    conversation = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship("User", backref="consultations")