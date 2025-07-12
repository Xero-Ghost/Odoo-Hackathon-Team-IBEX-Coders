from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(100))
    profile_photo = db.Column(db.String(200))
    availability = db.Column(db.String(200))
    is_public = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    unread_notifications = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills_offered = db.relationship('Skill', backref='user', lazy=True, cascade='all, delete-orphan')
    skills_wanted = db.relationship('SkillWanted', backref='user', lazy=True, cascade='all, delete-orphan')
    sent_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.requester_id', backref='requester', lazy=True)
    received_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.requested_id', backref='requested', lazy=True)
    given_feedback = db.relationship('Feedback', foreign_keys='Feedback.from_user_id', backref='from_user', lazy=True)
    received_feedback = db.relationship('Feedback', foreign_keys='Feedback.to_user_id', backref='to_user', lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def average_rating(self):
        ratings = [f.rating for f in self.received_feedback if f.rating]
        return round(sum(ratings) / len(ratings), 1) if ratings else 0
    
    @property
    def review_count(self):
        return len(self.received_feedback)
    
    def get_active_swaps(self):
        return SwapRequest.query.filter_by(requester_id=self.id, status='accepted').count() + \
               SwapRequest.query.filter_by(requested_id=self.id, status='accepted').count()
    
    def get_pending_requests(self):
        return SwapRequest.query.filter_by(requested_id=self.id, status='pending').count()
    
    def get_completed_swaps(self):
        return SwapRequest.query.filter_by(requester_id=self.id, status='completed').count() + \
               SwapRequest.query.filter_by(requested_id=self.id, status='completed').count()

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SkillWanted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_offered = db.Column(db.String(100), nullable=False)
    skill_wanted = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, completed, cancelled
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    swap_request_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)