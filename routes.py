"""
Jharkhand Tourism - API Routes
RESTful endpoints connecting frontend to backend services
"""

import os
from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
from services import (
    BookingService, DestinationService, ReviewService, UserService,
    ServiceManagementService, ChatService, AnalyticsService, AuthService
)
from models import db, User, Destination, Service, Booking, Review, OTPVerification, VerificationRequest
from utils import decode_jwt

ALLOWED_UPLOAD_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
DEFAULT_UPLOAD_FOLDER = 'uploads'

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_bp = Blueprint('user', __name__, url_prefix='/user')
dest_bp = Blueprint('destinations', __name__, url_prefix='/destinations')
booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')
service_bp = Blueprint('services', __name__, url_prefix='/services')
review_bp = Blueprint('reviews', __name__, url_prefix='/reviews')
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# Auth decorator
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])

    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ', 1)[1]
        payload = decode_jwt(token)
        if payload and payload.get('user_id'):
            return User.query.get(payload['user_id'])
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        return f(user, *args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(user, *args, **kwargs):
            if user.role not in allowed_roles:
                return jsonify({'status': 'error', 'message': 'Access denied'}), 403
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


# ===== AUTHENTICATION ROUTES =====
@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    payload = request.get_json(silent=True)
    if not payload:
        payload = request.form.to_dict()

    name = payload.get('name')
    email = payload.get('email')
    password = payload.get('password')
    confirm_password = payload.get('confirm_password')
    phone = payload.get('phone')
    role = payload.get('role', 'tourist')

    if not name or not email or not password or not confirm_password:
        return jsonify({'status': 'error', 'message': 'All required fields must be completed'}), 400

    if password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Passwords do not match'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already exists'}), 400

    document_path = None
    profile_image_path = None
    verification_required = role in ['guide', 'artisan', 'homestay_owner']

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')

    if 'profile_image' in request.files:
        profile_file = request.files['profile_image']
        if profile_file and allowed_file(profile_file.filename):
            filename = secure_filename(profile_file.filename)
            profile_image_path = os.path.join(upload_folder, filename)
            profile_file.save(profile_image_path)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid profile image upload'}), 400

    if 'id_document' in request.files:
        id_file = request.files['id_document']
        if id_file and allowed_file(id_file.filename):
            filename = secure_filename(id_file.filename)
            document_path = os.path.join(upload_folder, filename)
            id_file.save(document_path)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid ID document upload'}), 400

    try:
        user = AuthService.create_user(
            name=name,
            email=email,
            password=password,
            phone=phone,
            role=role,
            profile_pic=profile_image_path,
            id_document=document_path,
            requires_verification=verification_required
        )

        if verification_required and document_path:
            AuthService.request_verification(user.id, document_type='Government ID', document_path=document_path)

        AuthService.send_otp_email(user, purpose='signup')

        return jsonify({
            'status': 'success',
            'message': 'Registration successful. Check your email for the OTP code.',
            'user_id': user.id
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

    user = AuthService.get_user_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    if not user.verified:
        return jsonify({'status': 'error', 'message': 'Account is not verified. Please verify your email.'}), 403

    if user.role in ['guide', 'artisan', 'homestay_owner'] and user.verification_status != 'approved':
        return jsonify({'status': 'error', 'message': 'Account verification is pending admin approval.'}), 403

    remember_me = bool(data.get('remember_me', False))
    token = AuthService.create_auth_token(user)
    session.permanent = remember_me
    session['user_id'] = user.id
    session['user_role'] = user.role
    session['user_name'] = user.name

    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'user_id': user.id,
        'user_name': user.name,
        'user_role': user.role,
        'token': token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out'}), 200


@auth_bp.route('/me', methods=['GET'])
def me():
    """Return current authenticated user based on server session or token"""
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401

    return jsonify({
        'status': 'success',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    otp_code = data.get('otp')

    if not email or not otp_code:
        return jsonify({'status': 'error', 'message': 'Email and OTP are required'}), 400

    try:
        user = AuthService.verify_otp(email, otp_code, purpose='signup')
        return jsonify({
            'status': 'success',
            'message': 'Email verified successfully. You may now log in.',
            'user_id': user.id
        }), 200
    except ValueError as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 400
    except Exception as exc:
        return jsonify({'status': 'error', 'message': 'Verification failed'}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = data.get('email')

    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required'}), 400

    try:
        AuthService.request_password_reset(email)
        return jsonify({
            'status': 'success',
            'message': 'A password reset OTP has been sent to your email.'
        }), 200
    except ValueError as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 400
    except Exception as exc:
        return jsonify({'status': 'error', 'message': 'Unable to process password reset'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    otp_code = data.get('otp')
    new_password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not email or not otp_code or not new_password or not confirm_password:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Passwords do not match'}), 400

    try:
        AuthService.reset_password(email, otp_code, new_password)
        return jsonify({
            'status': 'success',
            'message': 'Password updated successfully. Please log in with your new password.'
        }), 200
    except ValueError as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 400
    except Exception as exc:
        return jsonify({'status': 'error', 'message': 'Unable to reset password'}), 500


@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile(user):
    return jsonify({'status': 'success', 'user': user.to_dict()}), 200


@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile(user):
    data = request.get_json(silent=True) or {}
    try:
        updated = UserService.update_user_profile(user.id, **data)
        return jsonify({'status': 'success', 'user': updated.to_dict()}), 200
    except Exception as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 500


@auth_bp.route('/verification-requests', methods=['GET'])
@login_required
@role_required('admin', 'government_official')
def get_verification_requests(user):
    requests = VerificationRequest.query.order_by(VerificationRequest.submitted_at.desc()).all()
    return jsonify({
        'status': 'success',
        'requests': [request_record.to_dict() for request_record in requests]
    }), 200


@auth_bp.route('/verification-requests/<int:request_id>/review', methods=['PUT'])
@login_required
@role_required('admin', 'government_official')
def review_verification_request(user, request_id):
    data = request.get_json(silent=True) or {}
    action = data.get('action', 'approve')
    notes = data.get('notes')
    approved = action == 'approve'
    try:
        record = AuthService.approve_verification_request(request_id, approved=approved, notes=notes)
        return jsonify({'status': 'success', 'verification_request': record.to_dict()}), 200
    except ValueError as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 404
    except Exception as exc:
        return jsonify({'status': 'error', 'message': 'Unable to update verification request'}), 500


# ===== USER ROUTES =====
@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile(user):
    """Get current user profile"""
    return jsonify({'status': 'success', 'user': user.to_dict()}), 200

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile(user):
    """Update user profile"""
    data = request.get_json()
    user = UserService.update_user_profile(user.id, **data)
    return jsonify({'status': 'success', 'user': user.to_dict()}), 200

# ===== DESTINATION ROUTES =====
@dest_bp.route('', methods=['GET'])
def get_destinations():
    """Get all destinations"""
    category = request.args.get('category')
    destinations = DestinationService.get_all_destinations(category)
    
    return jsonify({
        'status': 'success',
        'destinations': [d.to_dict() for d in destinations]
    }), 200

@dest_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    """Get single destination details"""
    dest = DestinationService.get_destination_by_id(destination_id)
    
    if not dest:
        return jsonify({'status': 'error', 'message': 'Destination not found'}), 404
    
    # Get services for this destination
    services = Service.query.filter_by(destination_id=destination_id).all()
    reviews = ReviewService.get_reviews_for_destination(destination_id)
    
    return jsonify({
        'status': 'success',
        'destination': dest.to_dict(),
        'services': [s.to_dict() for s in services],
        'reviews': [r.to_dict() for r in reviews]
    }), 200

@dest_bp.route('/search', methods=['GET'])
def search_destinations():
    """Search destinations"""
    keyword = request.args.get('q', '')
    results = DestinationService.search_destinations(keyword)
    
    return jsonify({
        'status': 'success',
        'results': [d.to_dict() for d in results]
    }), 200

# ===== BOOKING ROUTES =====
@booking_bp.route('', methods=['POST'])
@login_required
def create_booking(user):
    """Create a new booking"""
    data = request.get_json()
    
    try:
        booking = BookingService.create_booking(
            user_id=user.id,
            destination_id=data['destination_id'],
            service_id=data.get('service_id'),
            start_date=datetime.fromisoformat(data['start_date']).date(),
            end_date=datetime.fromisoformat(data['end_date']).date(),
            guests=data.get('guests', 1),
            total_price=data.get('total_price', 0),
            phone=data.get('phone'),
            accommodation_type=data.get('accommodation_type'),
            special_requests=data.get('special_requests')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Booking created',
            'booking_id': booking.id
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@booking_bp.route('', methods=['GET'])
@login_required
def get_bookings(user):
    """Get user's bookings"""
    status = request.args.get('status')
    bookings = BookingService.get_user_bookings(user.id, status)
    
    return jsonify({
        'status': 'success',
        'bookings': [b.to_dict() for b in bookings]
    }), 200

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@login_required
def get_booking(user, booking_id):
    """Get single booking details"""
    booking = Booking.query.get(booking_id)
    
    if not booking or booking.user_id != user.id:
        return jsonify({'status': 'error', 'message': 'Booking not found'}), 404
    
    return jsonify({
        'status': 'success',
        'booking': booking.to_dict()
    }), 200

@booking_bp.route('/<int:booking_id>/cancel', methods=['PUT'])
@login_required
def cancel_booking(user, booking_id):
    """Cancel a booking"""
    booking = Booking.query.get(booking_id)
    
    if not booking or booking.user_id != user.id:
        return jsonify({'status': 'error', 'message': 'Booking not found'}), 404
    
    booking = BookingService.update_booking_status(booking_id, 'cancelled')
    
    return jsonify({
        'status': 'success',
        'message': 'Booking cancelled',
        'booking': booking.to_dict()
    }), 200


@booking_bp.route('/<int:booking_id>/status', methods=['PUT'])
@login_required
@role_required('guide', 'artisan', 'homestay_owner', 'admin', 'government_official')
def update_booking_status(user, booking_id):
    """Update booking status for provider-managed or admin-managed bookings"""
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'status': 'error', 'message': 'Booking not found'}), 404

    if user.role in ['guide', 'artisan', 'homestay_owner']:
        if not booking.service or booking.service.provider_id != user.id:
            return jsonify({'status': 'error', 'message': 'Access denied'}), 403

    payload = request.get_json(silent=True) or {}
    status = payload.get('status')
    if status not in ['confirmed', 'cancelled', 'completed', 'rejected']:
        return jsonify({'status': 'error', 'message': 'Invalid status'}), 400

    updated_booking = BookingService.update_booking_status(booking_id, status)
    return jsonify({
        'status': 'success',
        'message': f'Booking {status}',
        'booking': updated_booking.to_dict()
    }), 200


# Development-only test booking endpoint: allows creating a booking without login for quick testing
@booking_bp.route('/test', methods=['POST'])
def create_test_booking():
    from flask import current_app
    # only allow in development
    if os.environ.get('FLASK_ENV') != 'development' and not current_app.debug:
        return jsonify({'status': 'error', 'message': 'Test booking is only available in development'}), 403

    data = request.get_json() or {}
    # pick or create a guest user
    guest = User.query.filter_by(email='guest@local.test').first()
    if not guest:
        guest = User(name='Guest User', email='guest@local.test', role='tourist')
        guest.set_password('guest')
        db.session.add(guest)
        db.session.commit()

    try:
        booking = BookingService.create_booking(
            user_id=guest.id,
            destination_id=data.get('destination_id') or 1,
            service_id=data.get('service_id'),
            start_date=datetime.fromisoformat(data.get('start_date')).date(),
            end_date=datetime.fromisoformat(data.get('end_date')).date(),
            guests=data.get('guests', 1),
            total_price=data.get('total_price', 0),
            phone=data.get('phone'),
            accommodation_type=data.get('accommodation_type'),
            special_requests=data.get('special_requests')
        )
        return jsonify({'status': 'success', 'message': 'Test booking created', 'booking_id': booking.id}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ===== SERVICE ROUTES =====
@service_bp.route('', methods=['POST'])
@login_required
@role_required('guide', 'artisan', 'homestay_owner')
def create_service(user):
    """Create a new service (Provider only)"""
    data = request.get_json()
    
    allowed_service_types = {
        'guide': ['guide'],
        'artisan': ['artisan'],
        'homestay_owner': ['homestay']
    }
    valid_types = allowed_service_types.get(user.role, [])
    requested_type = data.get('service_type')

    if requested_type not in valid_types:
        return jsonify({
            'status': 'error',
            'message': f"Invalid service type for your account. Allowed types: {', '.join(valid_types)}"
        }), 400

    try:
        service = ServiceManagementService.create_service(
            provider_id=user.id,
            destination_id=data['destination_id'],
            name=data['name'],
            service_type=requested_type,
            price_per_day=data['price_per_day'],
            description=data.get('description'),
            capacity=data.get('capacity')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Service created',
            'service_id': service.id
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@service_bp.route('/provider', methods=['GET'])
@login_required
@role_required('guide', 'artisan', 'homestay_owner')
def get_provider_services(user):
    """Get services for current provider"""
    services = ServiceManagementService.get_provider_services(user.id)
    
    return jsonify({
        'status': 'success',
        'services': [s.to_dict() for s in services]
    }), 200

@service_bp.route('/<int:service_id>', methods=['PUT'])
@login_required
@role_required('guide', 'artisan', 'homestay_owner')
def update_service(user, service_id):
    """Update a service"""
    service = Service.query.get(service_id)
    
    if not service or service.provider_id != user.id:
        return jsonify({'status': 'error', 'message': 'Not authorized'}), 403
    
    data = request.get_json()
    service = ServiceManagementService.update_service(service_id, **data)
    
    return jsonify({
        'status': 'success',
        'service': service.to_dict()
    }), 200

# ===== REVIEW ROUTES =====
@review_bp.route('', methods=['POST'])
@login_required
def create_review(user):
    """Create a review"""
    data = request.get_json()
    
    try:
        review = ReviewService.create_review(
            reviewer_id=user.id,
            rating=data['rating'],
            comment=data.get('comment'),
            destination_id=data.get('destination_id'),
            service_id=data.get('service_id'),
            verified_booking=data.get('verified_booking', False)
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Review created',
            'review_id': review.id
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@review_bp.route('/destination/<int:destination_id>', methods=['GET'])
def get_destination_reviews(destination_id):
    """Get reviews for a destination"""
    reviews = ReviewService.get_reviews_for_destination(destination_id)
    
    return jsonify({
        'status': 'success',
        'reviews': [r.to_dict() for r in reviews]
    }), 200

# ===== ANALYTICS ROUTES (Admin only) =====
@analytics_bp.route('/bookings', methods=['GET'])
@login_required
@role_required('admin', 'government_official')
def get_booking_analytics(user):
    """Get booking analytics"""
    stats = AnalyticsService.get_booking_stats()
    return jsonify({'status': 'success', 'data': stats}), 200

@analytics_bp.route('/destinations', methods=['GET'])
@login_required
@role_required('admin', 'government_official')
def get_destination_analytics(user):
    """Get destination analytics"""
    stats = AnalyticsService.get_destination_stats()
    return jsonify({'status': 'success', 'data': stats}), 200

@analytics_bp.route('/users', methods=['GET'])
@login_required
@role_required('admin', 'government_official')
def get_user_analytics(user):
    """Get user analytics"""
    stats = AnalyticsService.get_user_stats()
    return jsonify({'status': 'success', 'data': stats}), 200

@analytics_bp.route('/top-destinations', methods=['GET'])
def get_top_destinations():
    """Get top destinations"""
    destinations = AnalyticsService.get_top_destinations(10)
    
    return jsonify({
        'status': 'success',
        'destinations': [d.to_dict() for d in destinations]
    }), 200
