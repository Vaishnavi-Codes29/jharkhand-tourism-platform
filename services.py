"""
Jharkhand Tourism - Service Layer
Business logic and interconnected services
"""

from datetime import datetime, timedelta
from models import db, User, Destination, Service, Booking, Review, ChatHistory, OTPVerification, VerificationRequest
from sqlalchemy import or_, and_
from utils import (
    hash_password, check_password, create_otp_code, send_email,
    generate_jwt, is_valid_email, is_strong_password
)

class BookingService:
    """Handle booking operations and interconnections"""
    
    @staticmethod
    def create_booking(user_id, destination_id, service_id, start_date, end_date, guests, total_price, **kwargs):
        """Create a new booking and link to user and destination"""
        # capacity check: ensure service has enough capacity for requested dates
        service = Service.query.get(service_id) if service_id else None
        if service and service.capacity is not None:
            # find overlapping bookings for this service
            overlapping = Booking.query.filter(
                Booking.service_id == service_id,
                Booking.status != 'cancelled',
                Booking.start_date <= end_date,
                Booking.end_date >= start_date
            ).all()
            already_booked = sum((b.guests or 0) for b in overlapping)
            if already_booked + (guests or 0) > (service.capacity or 0):
                raise ValueError('Not enough availability for selected dates')

        booking = Booking(
            user_id=user_id,
            destination_id=destination_id,
            service_id=service_id,
            start_date=start_date,
            end_date=end_date,
            guests=guests,
            total_price=total_price,
            phone=kwargs.get('phone'),
            accommodation_type=kwargs.get('accommodation_type'),
            special_requests=kwargs.get('special_requests')
        )
        db.session.add(booking)
        db.session.commit()
        BookingService.update_service_availability(service_id)
        return booking
    
    @staticmethod
    def get_user_bookings(user_id, status=None):
        """Get all bookings for a user"""
        query = Booking.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()
    
    @staticmethod
    def update_booking_status(booking_id, status):
        """Update booking status"""
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = status
            booking.updated_at = datetime.utcnow()
            db.session.commit()
            BookingService.update_service_availability(booking.service_id)
        return booking
    
    @staticmethod
    def update_service_availability(service_id):
        service = Service.query.get(service_id)
        if not service:
            return

        if service.capacity is None:
            service.availability = True
        else:
            active_bookings = Booking.query.filter(
                Booking.service_id == service_id,
                Booking.status != 'cancelled'
            ).all()
            total_booked = sum((b.guests or 0) for b in active_bookings)
            service.availability = total_booked < (service.capacity or 0)

        db.session.commit()

    @staticmethod
    def get_provider_bookings(provider_id, status=None):
        """Get all bookings for a provider's services"""
        query = Booking.query.join(Service).filter(Service.provider_id == provider_id)
        if status:
            query = query.filter(Booking.status == status)
        return query.all()


class DestinationService:
    """Handle destination operations"""
    
    @staticmethod
    def get_all_destinations(category=None):
        """Get all destinations, optionally filtered by category"""
        query = Destination.query
        if category:
            query = query.filter_by(category=category)
        return query.all()
    
    @staticmethod
    def get_destination_by_id(destination_id):
        """Get destination details"""
        return Destination.query.get(destination_id)
    
    @staticmethod
    def search_destinations(keyword):
        """Search destinations by name or location"""
        return Destination.query.filter(
            or_(
                Destination.name.ilike(f'%{keyword}%'),
                Destination.location.ilike(f'%{keyword}%'),
                Destination.description.ilike(f'%{keyword}%')
            )
        ).all()
    
    @staticmethod
    def get_destinations_by_category(category):
        """Get all destinations in a category"""
        return Destination.query.filter_by(category=category).all()


class ReviewService:
    """Handle reviews and ratings"""
    
    @staticmethod
    def create_review(reviewer_id, rating, comment, destination_id=None, service_id=None, verified_booking=False):
        """Create a new review"""
        review = Review(
            reviewer_id=reviewer_id,
            rating=rating,
            comment=comment,
            destination_id=destination_id,
            service_id=service_id,
            verified_booking=verified_booking
        )
        db.session.add(review)
        
        # Update destination or service rating
        if destination_id:
            dest = Destination.query.get(destination_id)
            if dest:
                dest.review_count += 1
                old_rating = dest.rating
                dest.rating = ((old_rating * (dest.review_count - 1)) + rating) / dest.review_count
        
        if service_id:
            service = Service.query.get(service_id)
            if service:
                old_rating = service.rating
                service_reviews = Review.query.filter_by(service_id=service_id).count()
                service.rating = ((old_rating * service_reviews) + rating) / (service_reviews + 1)
        
        db.session.commit()
        return review
    
    @staticmethod
    def get_reviews_for_destination(destination_id):
        """Get all reviews for a destination"""
        return Review.query.filter_by(destination_id=destination_id).order_by(Review.created_at.desc()).all()
    
    @staticmethod
    def get_reviews_for_service(service_id):
        """Get all reviews for a service"""
        return Review.query.filter_by(service_id=service_id).order_by(Review.created_at.desc()).all()


class UserService:
    """Handle user operations"""
    
    @staticmethod
    def create_user(name, email, password, phone=None, role='tourist'):
        """Create a new user"""
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email and password"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """Update user profile"""
        user = User.query.get(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'password':
                    setattr(user, key, value)
            if 'password' in kwargs:
                user.set_password(kwargs['password'])
            user.updated_at = datetime.utcnow()
            db.session.commit()
        return user
    
    @staticmethod
    def get_provider_profile(provider_id):
        """Get provider profile with services"""
        provider = User.query.get(provider_id)
        if provider and provider.role == 'provider':
            return provider
        return None


class AuthService:
    """Handle secure authentication, OTP, and verification workflows"""

    @staticmethod
    def create_user(name, email, password, phone=None, role='tourist', profile_pic=None, id_document=None, requires_verification=False):
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already exists')

        if not is_valid_email(email):
            raise ValueError('Valid email is required')

        if not is_strong_password(password):
            raise ValueError('Password must have at least 8 characters, uppercase, lowercase, number and symbol')

        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            profile_pic=profile_pic,
            id_document=id_document,
            verification_status='pending' if requires_verification else 'pending',
            verified=False
        )
        user.set_password(password)

        if role in ['tourist', 'government_official', 'admin']:
            user.verification_status = 'pending'

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate_user(email, password):
        user = AuthService.get_user_by_email(email)
        if not user:
            return None
        if not user.check_password(password):
            return None
        if not user.verified:
            return None
        return user

    @staticmethod
    def create_auth_token(user):
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role
        }
        return generate_jwt(payload)

    @staticmethod
    def create_otp_record(user_id, purpose):
        code = create_otp_code()
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        otp = OTPVerification(
            user_id=user_id,
            purpose=purpose,
            otp_code=code,
            expires_at=expires_at
        )
        db.session.add(otp)
        db.session.commit()
        return otp

    @staticmethod
    def send_otp_email(user, purpose='signup'):
        otp = AuthService.create_otp_record(user.id, purpose)
        subject = 'Your Jharkhand Tourism verification code'
        body = (
            f"Hello {user.name},\n\n"
            f"Use this one-time code to complete your {purpose.replace('-', ' ')} process:\n\n"
            f"{otp.otp_code}\n\n"
            f"This code expires in 15 minutes.\n\n"
            "If you did not request this, please ignore this email.\n\n"
            "Jharkhand Tourism Team"
        )
        send_email(subject, user.email, body)
        return otp

    @staticmethod
    def verify_otp(email, otp_code, purpose='signup'):
        user = AuthService.get_user_by_email(email)
        if not user:
            raise ValueError('Invalid email address')

        otp = OTPVerification.query.filter_by(
            user_id=user.id,
            purpose=purpose,
            otp_code=otp_code,
            verified=False
        ).order_by(OTPVerification.created_at.desc()).first()

        if not otp or otp.expires_at < datetime.utcnow():
            raise ValueError('OTP is invalid or expired')

        otp.verified = True
        user.verified = True
        user.verification_status = 'approved' if user.role in ['tourist', 'government_official', 'admin'] else 'pending'
        db.session.commit()
        return user

    @staticmethod
    def request_password_reset(email):
        user = AuthService.get_user_by_email(email)
        if not user:
            raise ValueError('Account not found')

        otp = AuthService.send_otp_email(user, purpose='reset-password')
        return otp

    @staticmethod
    def reset_password(email, otp_code, new_password):
        if not is_strong_password(new_password):
            raise ValueError('Password must have at least 8 characters, uppercase, lowercase, number and symbol')

        user = AuthService.get_user_by_email(email)
        if not user:
            raise ValueError('Account not found')

        otp = OTPVerification.query.filter_by(
            user_id=user.id,
            purpose='reset-password',
            otp_code=otp_code,
            verified=False
        ).order_by(OTPVerification.created_at.desc()).first()

        if not otp or otp.expires_at < datetime.utcnow():
            raise ValueError('OTP is invalid or expired')

        otp.verified = True
        user.set_password(new_password)
        db.session.commit()
        return user

    @staticmethod
    def request_verification(user_id, document_type=None, document_path=None):
        request_record = VerificationRequest(
            user_id=user_id,
            document_type=document_type,
            document_path=document_path,
            status='pending'
        )
        db.session.add(request_record)
        db.session.commit()
        return request_record

    @staticmethod
    def approve_verification_request(request_id, approved=True, notes=None):
        request_record = VerificationRequest.query.get(request_id)
        if not request_record:
            raise ValueError('Verification request not found')

        request_record.status = 'approved' if approved else 'rejected'
        request_record.review_notes = notes
        request_record.updated_at = datetime.utcnow()
        request_record.user.verification_status = request_record.status
        request_record.user.verified = approved
        db.session.commit()
        return request_record


class ServiceManagementService:
    """Handle service management for providers"""
    
    @staticmethod
    def create_service(provider_id, destination_id, name, service_type, price_per_day, **kwargs):
        """Create a new service"""
        service = Service(
            provider_id=provider_id,
            destination_id=destination_id,
            name=name,
            service_type=service_type,
            price_per_day=price_per_day,
            description=kwargs.get('description'),
            price_per_person=kwargs.get('price_per_person'),
            capacity=kwargs.get('capacity')
        )
        db.session.add(service)
        db.session.commit()
        return service
    
    @staticmethod
    def get_provider_services(provider_id):
        """Get all services for a provider"""
        return Service.query.filter_by(provider_id=provider_id).all()
    
    @staticmethod
    def update_service(service_id, **kwargs):
        """Update service details"""
        service = Service.query.get(service_id)
        if service:
            for key, value in kwargs.items():
                if hasattr(service, key):
                    setattr(service, key, value)
            db.session.commit()
        return service
    
    @staticmethod
    def delete_service(service_id):
        """Delete a service"""
        service = Service.query.get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return True
        return False


class ChatService:
    """Handle chat history with AI"""
    
    @staticmethod
    def save_chat_message(user_id, message, response):
        """Save chat history"""
        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=response
        )
        db.session.add(chat)
        db.session.commit()
        return chat
    
    @staticmethod
    def get_user_chat_history(user_id, limit=50):
        """Get chat history for a user"""
        return ChatHistory.query.filter_by(user_id=user_id).order_by(
            ChatHistory.created_at.desc()
        ).limit(limit).all()


class AnalyticsService:
    """Handle analytics and reporting"""
    
    @staticmethod
    def get_booking_stats():
        """Get booking statistics"""
        total_bookings = Booking.query.count()
        confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
        completed_bookings = Booking.query.filter_by(status='completed').count()
        total_revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0
        
        return {
            'total_bookings': total_bookings,
            'confirmed': confirmed_bookings,
            'completed': completed_bookings,
            'revenue': total_revenue
        }
    
    @staticmethod
    def get_top_destinations(limit=10):
        """Get top destinations by reviews"""
        return Destination.query.order_by(Destination.rating.desc()).limit(limit).all()
    
    @staticmethod
    def get_user_stats():
        """Get user statistics"""
        total_users = User.query.count()
        tourists = User.query.filter_by(role='tourist').count()
        providers = User.query.filter_by(role='provider').count()
        verified_providers = User.query.filter_by(role='provider', verified=True).count()
        
        return {
            'total_users': total_users,
            'tourists': tourists,
            'providers': providers,
            'verified_providers': verified_providers
        }
    
    @staticmethod
    def get_destination_stats():
        """Get destination statistics"""
        total_destinations = Destination.query.count()
        by_category = db.session.query(
            Destination.category,
            db.func.count(Destination.id)
        ).group_by(Destination.category).all()
        
        return {
            'total_destinations': total_destinations,
            'by_category': dict(by_category)
        }
