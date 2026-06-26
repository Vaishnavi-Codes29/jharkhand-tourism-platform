"""
Jharkhand Tourism - Database Models
Defines SQLAlchemy models for users, bookings, destinations, and services
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from utils import hash_password, check_password

db = SQLAlchemy()

class User(db.Model):
    """User model for tourists, providers, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(30), default='tourist')  # tourist, guide, artisan, homestay_owner, admin, government_official
    profile_pic = db.Column(db.String(255))
    id_document = db.Column(db.String(255))
    verification_status = db.Column(db.String(30), default='none')  # none, pending, approved, rejected
    bio = db.Column(db.Text)
    city = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    bookings = db.relationship('Booking', foreign_keys='Booking.user_id', backref='tourist', lazy=True)
    services = db.relationship('Service', backref='provider', lazy=True)
    reviews = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        return check_password(password, self.password_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'verified': self.verified,
            'verification_status': self.verification_status,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'city': self.city,
            'created_at': self.created_at.isoformat()
        }


class OTPVerification(db.Model):
    """One-time password and verification records"""
    __tablename__ = 'otp_verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    purpose = db.Column(db.String(50), nullable=False)
    otp_code = db.Column(db.String(10), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('otp_records', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'purpose': self.purpose,
            'verified': self.verified,
            'expires_at': self.expires_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class VerificationRequest(db.Model):
    """Provider verification requests for guides, artisans, and homestay owners"""
    __tablename__ = 'verification_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(80), nullable=True)
    document_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), default='pending')
    review_notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('verification_requests', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'document_path': self.document_path,
            'status': self.status,
            'review_notes': self.review_notes,
            'submitted_at': self.submitted_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Destination(db.Model):
    """Destination model for tourist attractions"""
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # waterfall, temple, wildlife, etc.
    description = db.Column(db.Text)
    location = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    best_time = db.Column(db.String(100))
    entry_fee = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    
    # Relationships
    bookings = db.relationship('Booking', backref='destination', lazy=True)
    services = db.relationship('Service', backref='destination', lazy=True)
    reviews = db.relationship('Review', foreign_keys='Review.destination_id', backref='destination', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'location': self.location,
            'best_time': self.best_time,
            'entry_fee': self.entry_fee,
            'image_url': self.image_url,
            'rating': self.rating
        }


class Service(db.Model):
    """Service model for provider offerings"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    service_type = db.Column(db.String(50))  # hotel, guide, transport, food, activity
    price_per_day = db.Column(db.Float, nullable=False)
    price_per_person = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0)
    availability = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='service', lazy=True)
    reviews = db.relationship('Review', foreign_keys='Review.service_id', backref='service', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'service_type': self.service_type,
            'price_per_day': self.price_per_day,
            'rating': self.rating,
            'availability': self.availability
        }


class Booking(db.Model):
    """Booking model for reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    
    accommodation_type = db.Column(db.String(50))
    special_requests = db.Column(db.Text)
    phone = db.Column(db.String(20))
    
    # Relationships
    payments = db.relationship('Payment', backref='booking', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination.name if self.destination else None,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'guests': self.guests,
            'total_price': self.total_price,
            'status': self.status
        }


class Payment(db.Model):
    """Payment model for transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, upi, net_banking
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    transaction_id = db.Column(db.String(100), unique=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Review(db.Model):
    """Review model for ratings and feedback"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    verified_booking = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'reviewer': self.reviewer.name if self.reviewer else 'Anonymous',
            'created_at': self.created_at.isoformat()
        }


class ChatHistory(db.Model):
    """Chat history with AI guide"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
