from pathlib import Path
from routes import auth_bp, user_bp, dest_bp, booking_bp, service_bp, review_bp, analytics_bp
from services import (
    UserService, DestinationService, BookingService, ReviewService,
    ServiceManagementService, ChatService, AnalyticsService
)
from models import db, User, Destination, Service, Booking, Review, ChatHistory, VerificationRequest
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
from functools import wraps
from sqlalchemy import or_
import os
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')
if not (BASE_DIR / '.env').exists() and (BASE_DIR / '.env.example').exists():
    load_dotenv(BASE_DIR / '.env.example')

# Import models and services

# Flask app initialization
app = Flask(__name__)
CORS(app)

# ===== CONFIGURATION =====
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# ===== GROQ CONFIGURATION =====
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CHAT_MODEL = os.environ.get("CHAT_MODEL", "llama3-8b-8192")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured. Create a .env file in the project root "
        "with GROQ_API_KEY=<your-key> and SECRET_KEY=<your-secret>. "
        "If you do not have a .env file, copy .env.example to .env first."
    )

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

# Flask configuration
app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.permanent_session_lifetime = timedelta(days=30)
# Session cookie settings - adjust for local development (set SECURE=True in production)
app.config['SESSION_COOKIE_SAMESITE'] = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = True

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(dest_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(service_bp)
app.register_blueprint(review_bp)
app.register_blueprint(analytics_bp)

# ===== CHAT SYSTEM PROMPT =====
CHAT_SYSTEM_PROMPT = """
You are a friendly, knowledgeable AI travel guide for Jharkhand Tourism — a state in eastern India known for its stunning waterfalls, tribal heritage, ancient forests, wildlife, and rich culture.

Your name is "Jharkhand AI Guide".

Key facts about Jharkhand:
- Capital: Ranchi
- Major cities: Jamshedpur, Dhanbad, Bokaro, Hazaribagh, Dumka
- Famous waterfalls: Hundru Falls, Dassam Falls, Jonha Falls, Lodh Falls
- Wildlife: Betla National Park, Dalma Wildlife Sanctuary
- Culture: Tribal communities, Chhau dance, Sohrai paintings
- Religious sites: Deoghar, Parasnath Hill, Itkhori Temple
- Best time to visit: October to March
- Cuisine: Thekua, Dhuska, Rugra

Respond helpfully, warmly, and concisely.
Use bullet points when listing items.
Keep responses under 200 words unless more detail is needed.
Use emojis where suitable.
"""

# ===== DATABASE INITIALIZATION =====


@app.before_request
def create_tables():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()

# ===== HOME PAGE =====


@app.route('/')
def home():
    if session.get('user_id'):
        return redirect(get_home_url())
    return render_template("index.html")


@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/forgot-password')
def forgot_password_page():
    return render_template("forgot_password.html")


@app.route('/reset-password')
def reset_password_page():
    return render_template("reset_password.html")


@app.route('/verify-otp')
def verify_otp_page():
    return render_template("verify_otp.html")


def auth_page_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    return User.query.get(session['user_id']) if session.get('user_id') else None


def get_home_url():
    role = session.get('user_role')
    if role == 'tourist':
        return url_for('tourist_dashboard')
    if role == 'homestay_owner':
        return url_for('homestay_dashboard')
    if role in ['guide', 'artisan']:
        return url_for('provider_dashboard_page')
    if role in ['admin', 'government_official']:
        return url_for('admin_dashboard_page')
    if session.get('user_id'):
        return url_for('profile_page')
    return url_for('home')


def role_page_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('user_role') not in allowed_roles:
                return redirect(url_for('login_page'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/profile')
@auth_page_required
def profile_page():
    return render_template("profile.html")


@app.route('/admin_dashboard')
@role_page_required('admin', 'government_official')
def admin_dashboard_page():
    booking_stats = AnalyticsService.get_booking_stats()
    user_stats = AnalyticsService.get_user_stats()
    dest_stats = AnalyticsService.get_destination_stats()
    pending_approvals = VerificationRequest.query.filter_by(status='pending').order_by(VerificationRequest.submitted_at.desc()).limit(6).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(8).all()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(8).all()
    service_count = Service.query.count()
    monthly_bookings = Booking.query.filter(Booking.created_at >= datetime.utcnow() - timedelta(days=30)).count()
    avg_rating = db.session.query(db.func.avg(Destination.rating)).scalar() or 0
    prior_users = User.query.filter(User.created_at < datetime.utcnow() - timedelta(days=30)).count()
    user_growth = 0
    if prior_users > 0:
        user_growth = round(((user_stats['total_users'] - prior_users) / prior_users) * 100, 1)

    return render_template(
        "admin_dashboard.html",
        booking_stats=booking_stats,
        user_stats=user_stats,
        dest_stats=dest_stats,
        pending_approvals=pending_approvals,
        recent_users=recent_users,
        recent_bookings=recent_bookings,
        service_count=service_count,
        monthly_bookings=monthly_bookings,
        avg_rating=round(avg_rating, 1),
        user_growth=user_growth
    )


@app.route('/admin/bookings')
@role_page_required('admin', 'government_official')
def admin_bookings_data():
    status = request.args.get('status')
    provider_role = request.args.get('provider_role')
    search = request.args.get('q', '').strip()
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    query = Booking.query.join(Service).join(User, Service.provider_id == User.id)
    if status:
        query = query.filter(Booking.status == status)
    if provider_role:
        query = query.filter(User.role == provider_role)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Booking.destination.has(Destination.name.ilike(search_term)),
                Booking.tourist.has(User.name.ilike(search_term)),
                Booking.service.has(Service.name.ilike(search_term)),
                User.name.ilike(search_term)
            )
        )
    if from_date:
        try:
            query = query.filter(Booking.created_at >= datetime.fromisoformat(from_date))
        except ValueError:
            pass
    if to_date:
        try:
            query = query.filter(Booking.created_at <= datetime.fromisoformat(to_date))
        except ValueError:
            pass

    bookings = query.order_by(Booking.created_at.desc()).all()

    return jsonify({
        'status': 'success',
        'bookings': [
            {
                'id': b.id,
                'destination': b.destination.name if b.destination else 'Unknown',
                'tourist': b.tourist.name if b.tourist else 'Guest',
                'tourist_email': b.tourist.email if b.tourist else None,
                'provider': b.service.provider.name if b.service and b.service.provider else 'N/A',
                'provider_role': b.service.provider.role if b.service and b.service.provider else None,
                'service_name': b.service.name if b.service else None,
                'start_date': b.start_date.isoformat(),
                'end_date': b.end_date.isoformat(),
                'created_at': b.created_at.isoformat(),
                'status': b.status,
                'total_price': b.total_price or 0,
                'guests': b.guests,
                'accommodation_type': b.accommodation_type,
                'special_requests': b.special_requests
            }
            for b in bookings
        ]
    }), 200


@app.route('/provider_dashboard')
@role_page_required('guide', 'artisan', 'homestay_owner')
def provider_dashboard_page():
    user = get_current_user()
    if user.role == 'homestay_owner':
        return redirect(url_for('homestay_dashboard'))
    provider_services = ServiceManagementService.get_provider_services(user.id)
    provider_bookings = BookingService.get_provider_bookings(user.id)
    pending_bookings = [b for b in provider_bookings if b.status == 'pending']
    confirmed_bookings = [b for b in provider_bookings if b.status == 'confirmed']
    provider_revenue = sum((b.total_price or 0) for b in provider_bookings)

    return render_template(
        "provider_dashboard.html",
        provider_services=provider_services,
        provider_bookings=provider_bookings,
        dashboard_stats={
            'total_bookings': len(provider_bookings),
            'pending_bookings': len(pending_bookings),
            'confirmed_bookings': len(confirmed_bookings),
            'revenue': provider_revenue
        }
    )


@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('home'))


# ===== HOMESTAY DASHBOARD =====


@app.route('/homestay_dashboard')
@role_page_required('homestay_owner')
def homestay_dashboard():
    user = get_current_user()
    homestay_services = ServiceManagementService.get_provider_services(user.id)
    homestay_bookings = BookingService.get_provider_bookings(user.id)
    booking_stats = {
        'total_bookings': len(homestay_bookings),
        'confirmed_bookings': len([b for b in homestay_bookings if b.status == 'confirmed']),
        'pending_bookings': len([b for b in homestay_bookings if b.status == 'pending']),
        'revenue': sum((b.total_price or 0) for b in homestay_bookings)
    }

    tribe_colors = {
        'Santhal': 'linear-gradient(135deg,#2d5a27,#1a3520)',
        'Munda': 'linear-gradient(135deg,#7a3e1a,#4a2510)',
        'Oraon': 'linear-gradient(135deg,#4a7c3f,#2d5a27)',
        'Ho': 'linear-gradient(135deg,#1a5060,#0d3040)',
        'Kharia': 'linear-gradient(135deg,#5c3d1e,#3a2510)',
        'Birhor': 'linear-gradient(135deg,#2a4020,#1a2c14)'
    }

    homestay_services_data = []
    for service in homestay_services:
        destination = service.destination
        location = destination.location if destination else 'Jharkhand'
        tribe = destination.category.title() if destination and destination.category else 'Local'
        tribe = tribe if tribe in tribe_colors else 'Local'
        # compute available capacity (exclude cancelled bookings)
        booked_count = sum((b.guests or 0) for b in Booking.query.filter(Booking.service_id == service.id, Booking.status != 'cancelled').all())
        capacity = service.capacity or 0
        available = max(0, capacity - booked_count) if capacity else None

        homestay_services_data.append({
            'id': service.id,
            'name': service.name,
            'village': location,
            'district': location,
            'tribe': tribe,
            'price': round(service.price_per_day or service.price_per_person or 0),
            'capacity': capacity,
            'available': available,
            'rating': round(service.rating or 4.2, 1),
            'reviews': len(service.reviews) if service.reviews is not None else 0,
            'emoji': '🏡',
            'bgColor': tribe_colors.get(tribe, 'linear-gradient(135deg,#244965,#1f3549)'),
            'desc': service.description or f"Comfortable homestay experience with local hospitality.",
            'amenities': [
                f"₹{round(service.price_per_day or service.price_per_person or 0)}/night",
                f"{service.service_type.capitalize() if service.service_type else 'Homestay'}",
                'Family-hosted',
                'Traditional meals'
            ],
            'food': ['Seasonal Cuisine', 'Tribal Specialties'],
            'attractions': [destination.name if destination else 'Local Village'],
            'tags': [tribe, 'Eco Stay', 'Local Host']
        })

    homestay_bookings_data = []
    for booking in homestay_bookings:
        homestay_bookings_data.append({
            'id': booking.id,
            'service_name': booking.service.name if booking.service else 'Homestay',
            'destination_name': booking.destination.name if booking.destination else '',
            'start_date': booking.start_date.isoformat() if booking.start_date else None,
            'end_date': booking.end_date.isoformat() if booking.end_date else None,
            'guests': booking.guests,
            'status': booking.status,
            'total_price': round(booking.total_price or 0),
            'phone': booking.phone,
            'accommodation_type': booking.accommodation_type,
            'special_requests': booking.special_requests or '',
            'created_at': booking.created_at.strftime('%d %b %Y')
        })

    return render_template(
        "homestay_dashboard.html",
        homestay_services_data=homestay_services_data,
        homestay_bookings_data=homestay_bookings_data,
        booking_stats=booking_stats,
        home_url=get_home_url(),
        # force public listing view for /homestays (always show tourist-facing listing)
        user_role='tourist'
    )


@app.route('/homestays')
def homestays_public():
    # Homestays dashboard for tourists to browse available homestays

    tribe_colors = {
        'Santhal': 'linear-gradient(135deg,#2d5a27,#1a3520)',
        'Munda': 'linear-gradient(135deg,#7a3e1a,#4a2510)',
        'Oraon': 'linear-gradient(135deg,#4a7c3f,#2d5a27)',
        'Ho': 'linear-gradient(135deg,#1a5060,#0d3040)',
        'Kharia': 'linear-gradient(135deg,#5c3d1e,#3a2510)',
        'Birhor': 'linear-gradient(135deg,#2a4020,#1a2c14)'
    }

    services = Service.query.filter(Service.availability == True).all()
    homestay_services_data = []
    for service in services:
        destination = service.destination
        location = destination.location if destination else 'Jharkhand'
        tribe = destination.category.title() if destination and destination.category else 'Local'
        tribe = tribe if tribe in tribe_colors else 'Local'
        booked_count = sum((b.guests or 0) for b in Booking.query.filter(Booking.service_id == service.id, Booking.status != 'cancelled').all())
        capacity = service.capacity or 0
        available = max(0, capacity - booked_count) if capacity else None

        homestay_services_data.append({
            'id': service.id,
            'name': service.name,
            'village': location,
            'district': location,
            'tribe': tribe,
            'price': round(service.price_per_day or service.price_per_person or 0),
            'capacity': capacity,
            'available': available,
            'rating': round(service.rating or 4.2, 1),
            'reviews': len(service.reviews) if service.reviews is not None else 0,
            'emoji': '🏡',
            'bgColor': tribe_colors.get(tribe, 'linear-gradient(135deg,#244965,#1f3549)'),
            'desc': service.description or f"Comfortable homestay experience with local hospitality.",
            'amenities': [
                f"₹{round(service.price_per_day or service.price_per_person or 0)}/night",
                f"{service.service_type.capitalize() if service.service_type else 'Homestay'}",
                'Family-hosted',
                'Traditional meals'
            ],
            'food': ['Seasonal Cuisine', 'Tribal Specialties'],
            'attractions': [destination.name if destination else 'Local Village'],
            'tags': [tribe, 'Eco Stay', 'Local Host']
        })

    # public view does not include provider bookings
    homestay_bookings_data = []
    booking_stats = {'total_bookings': 0, 'confirmed_bookings': 0, 'pending_bookings': 0, 'revenue': 0}

    return render_template(
        "homestay_dashboard.html",
        homestay_services_data=homestay_services_data,
        homestay_bookings_data=homestay_bookings_data,
        booking_stats=booking_stats,
        home_url=get_home_url(),
        user_role=session.get('user_role')
    )


@app.route('/map')
def map_page():
    destinations = Destination.query.filter(
        Destination.latitude.isnot(None),
        Destination.longitude.isnot(None)
    ).all()

    destination_markers = [
        {
            'id': dest.id,
            'name': dest.name,
            'location': dest.location,
            'category': dest.category,
            'description': dest.description or 'Beautiful Jharkhand destination',
            'latitude': dest.latitude,
            'longitude': dest.longitude,
            'rating': round(dest.rating or 4.2, 1)
        }
        for dest in destinations
    ]

    return render_template(
        'map.html',
        destinations=destination_markers,
        home_url=get_home_url(),
        user_role=session.get('user_role')
    )


# ===== TOURIST DASHBOARD =====


@app.route('/tourist_dashboard')
@role_page_required('tourist')
def tourist_dashboard():
    user = get_current_user()
    book_choices = BookingService.get_user_bookings(user.id)
    favorite_count = 0
    review_count = Review.query.filter_by(reviewer_id=user.id).count()
    active_bookings = [b for b in book_choices if b.status != 'cancelled']

    return render_template(
        "tourist_dashboard.html",
        active_bookings=active_bookings,
        favorite_count=favorite_count,
        review_count=review_count,
        all_bookings=book_choices
    )


# ===== AI CHATBOT ENDPOINT =====


@app.route('/chat', methods=['POST'])
def chat():
    """AI-powered travel chatbot using Groq"""

    data = request.json
    messages = data.get('messages', [])

    if not messages:
        return jsonify({
            "status": "fail",
            "message": "No messages provided"
        }), 400

    if not GROQ_API_KEY:
        return jsonify({
            "status": "fail",
            "message": "Groq API key not configured"
        }), 500

    try:
        completion = client.chat.completions.create(
            model=CHAT_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": CHAT_SYSTEM_PROMPT
                },
                *messages[-20:]
            ],

            temperature=0.7,
            max_tokens=1000
        )

        reply = completion.choices[0].message.content

        # ===== SAVE CHAT HISTORY =====
        try:
            user_id = session.get('user', {}).get(
                'id') if session.get('user') else None

            ChatService.save_chat_message(
                user_id,
                'user',
                messages[-1]['content']
            )

            ChatService.save_chat_message(
                user_id,
                'assistant',
                reply
            )

        except Exception as e:
            print(f"Warning: Could not save chat history: {e}")

        return jsonify({
            "status": "success",
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "status": "fail",
            "message": str(e)
        }), 500


# ===== APPLICATION ENTRY POINT =====
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))

    app.run(
        debug=True,
        host=host,
        port=port
    )
