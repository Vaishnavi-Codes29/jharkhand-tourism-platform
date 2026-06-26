# Jharkhand Tourism Platform - Interconnectivity Guide

## Overview
This document describes the complete interconnected architecture of the Jharkhand Tourism Flask application, showing how all components (models, services, routes, and frontend) work together to provide a seamless user experience.

---

## Architecture Layers

### 1. **Data Layer (models.py)**
Defines the database schema using SQLAlchemy ORM with proper relationships and constraints.

#### Core Models & Relationships:
```
User
├── Bookings (one-to-many)
├── Reviews (one-to-many)
└── ChatHistory (one-to-many)

Destination
├── Services (one-to-many)
├── Bookings (one-to-many)
├── Reviews (one-to-many)
└── Ratings (auto-calculated)

Service (Provider Services)
├── Provider/User (many-to-one)
├── Destination (many-to-one)
├── Bookings (one-to-many)
├── Reviews (one-to-many)
└── Ratings (auto-calculated)

Booking
├── Tourist/User (many-to-one)
├── Destination (many-to-one)
├── Service (many-to-one)
└── Status Tracking (pending→confirmed→completed)

Review
├── Reviewer/User (many-to-one)
├── Destination (many-to-one)
├── Service (many-to-one)
└── Auto-updates ratings

ChatHistory
└── User (many-to-one) - Stores AI conversations
```

---

### 2. **Business Logic Layer (services.py)**
Implements core business operations with proper validation and error handling.

#### Service Classes & Operations:

##### **UserService**
- `register_user(name, email, password, role)` - Create new user account
- `authenticate_user(email, password)` - Verify credentials
- `get_user_profile(user_id)` - Fetch user details
- `update_user_profile(user_id, **kwargs)` - Update user info
- `verify_user_email(user_id)` - Mark email as verified

##### **DestinationService**
- `get_all_destinations()` - List all attractions
- `get_destination(dest_id)` - Fetch destination details
- `search_destinations(keyword)` - Search by name/category
- `get_destinations_by_category(category)` - Filter by type

##### **BookingService**
- `create_booking(user_id, dest_id, service_id, dates, guests)` - Create new booking
- `get_user_bookings(user_id)` - Fetch bookings for user
- `cancel_booking(booking_id)` - Cancel confirmed booking
- `update_booking_status(booking_id, status)` - Admin status update

##### **ReviewService**
- `create_review(user_id, destination_id, service_id, rating, comment)` - Submit review
- `get_reviews(destination_id)` - Fetch destination reviews
- `update_rating(destination_id, service_id)` - Auto-recalculate ratings
- `get_average_rating(destination_id)` - Calculate average rating

##### **ServiceManagementService**
- `create_service(provider_id, destination_id, name, service_type, price, capacity)` - Add service
- `get_provider_services(provider_id)` - List provider's offerings
- `update_service(service_id, **kwargs)` - Modify service details
- `delete_service(service_id)` - Remove service

##### **ChatService**
- `save_chat_message(user_id, role, content)` - Store chat history
- `get_chat_history(user_id)` - Retrieve conversation
- `clear_chat_history(user_id)` - Delete old messages

##### **AnalyticsService**
- `get_booking_stats()` - Admin: booking metrics
- `get_user_stats()` - Admin: user growth
- `get_destination_stats()` - Admin: popular attractions
- `get_revenue_stats()` - Admin: financial overview

---

### 3. **API Layer (routes.py)**
Organizes endpoints into feature blueprints with proper authentication & authorization.

#### Blueprint Structure (7 Blueprints, 50+ Endpoints):

##### **auth_bp** - Authentication
```
POST   /api/register              - Create new account
POST   /api/login                 - User login
POST   /api/logout                - User logout
GET    /api/check-session         - Verify login status
```

##### **user_bp** - User Management
```
GET    /api/user/profile          - Fetch user details
PUT    /api/user/profile          - Update user info
GET    /api/user/bookings         - List user's bookings
GET    /api/user/favorites        - Get saved destinations
POST   /api/user/favorites/<id>   - Add to favorites
```

##### **dest_bp** - Destinations
```
GET    /api/destinations          - List all attractions
GET    /api/destinations/<id>     - Fetch destination details
GET    /api/destinations/search   - Search by keyword
GET    /api/destinations/category/<cat> - Filter by category
```

##### **booking_bp** - Bookings
```
POST   /api/bookings              - Create new booking
GET    /api/bookings              - List user's bookings
GET    /api/bookings/<id>         - Fetch booking details
PUT    /api/bookings/<id>/cancel  - Cancel booking
POST   /api/bookings/<id>/review  - Submit review after completion
```

##### **service_bp** - Provider Services
```
POST   /api/services              - Create new service
GET    /api/services              - List all services
GET    /api/services/provider     - List provider's services
PUT    /api/services/<id>         - Update service details
DELETE /api/services/<id>         - Remove service
```

##### **review_bp** - Reviews & Ratings
```
POST   /api/reviews               - Submit review
GET    /api/reviews/destination/<id> - Fetch destination reviews
GET    /api/reviews/service/<id>  - Fetch service reviews
PUT    /api/reviews/<id>          - Edit review
DELETE /api/reviews/<id>          - Delete review
```

##### **analytics_bp** - Admin Analytics (Role-Based Access Control)
```
GET    /api/analytics/dashboard   - Admin dashboard overview
GET    /api/analytics/bookings    - Booking statistics
GET    /api/analytics/users       - User metrics
GET    /api/analytics/revenue     - Financial reports
GET    /api/analytics/destinations - Popular attractions
```

---

### 4. **Presentation Layer (Frontend Templates)**

#### Template Files & Their Functions:

| File | Purpose | Key Features |
|------|---------|--------------|
| **navbar.html** | Navigation bar | Dynamic login/logout, role-based menu |
| **index.html** | Home page | Hero section, destination grid, chatbot, search |
| **login.html** | Login form | Email/password, role selection, error messages |
| **register.html** | Registration | Multi-step form, password strength meter, role selection |
| **tourist_dashboard.html** | Tourist profile | Bookings, favorites, recommendations, profile |
| **provider_dashboard.html** | Provider profile | Services management, booking requests, analytics |
| **admin_dashboard.html** | Admin panel | User mgmt, booking mgmt, provider approvals, stats |
| **booking.html** | Booking form | Date picker, guest counter, dynamic pricing |
| **provider_profile.html** | Provider info | Business details, service listings, ratings |

---

## Data Flow & Integration

### **User Registration Flow**
```
1. User fills registration form (register.html)
   ↓
2. Frontend calls POST /api/register with form data
   ↓
3. routes.py (auth_bp) receives request → validates input
   ↓
4. Calls UserService.register_user(name, email, password, role)
   ↓
5. Service creates User model instance, validates uniqueness
   ↓
6. Database (SQLAlchemy) persists User record
   ↓
7. Session established, user redirected to dashboard
```

### **Booking Creation Flow**
```
1. Tourist selects destination & fills booking.html form
   ↓
2. Frontend calls POST /api/bookings with:
   - destination_id, service_id, dates, guests
   ↓
3. routes.py (booking_bp) validates user authentication
   ↓
4. Calls BookingService.create_booking(...)
   ↓
5. Service validates:
   - User exists & is verified
   - Destination/Service exist
   - Dates are available
   - Price calculation
   ↓
6. Creates Booking model with status='pending'
   ↓
7. Database persists Booking with relationships:
   - Links to User, Destination, Service
   ↓
8. Response sent to frontend with booking confirmation
   ↓
9. Admin receives notification in admin_dashboard.html
```

### **Review & Rating Flow**
```
1. Completed booking shows "Write Review" button
   ↓
2. Tourist submits review (rating + comment)
   ↓
3. Frontend calls POST /api/reviews with:
   - booking_id, destination_id, service_id, rating, comment
   ↓
4. routes.py (review_bp) validates authentication
   ↓
5. Calls ReviewService.create_review(...)
   ↓
6. Service creates Review model instance
   ↓
7. Automatically calls update_rating() to recalculate averages:
   - Sum all ratings for destination
   - Update Destination.rating field
   - Update Service.rating field
   ↓
8. Ratings display updated on destination_dashboard.html
   ↓
9. Provider sees updated ratings in provider_dashboard.html
```

### **Admin Analytics Flow**
```
1. Admin logs in with role='admin'
   ↓
2. Navigates to admin_dashboard.html
   ↓
3. Dashboard calls GET /api/analytics/dashboard
   ↓
4. routes.py (analytics_bp) checks: session['user']['role'] == 'admin'
   ↓
5. Calls AnalyticsService methods:
   - get_booking_stats() → Queries all Booking records
   - get_user_stats() → Queries all User records
   - get_destination_stats() → Queries Destination + reviews
   - get_revenue_stats() → Sum all booking amounts
   ↓
6. Services aggregate data from models using SQLAlchemy queries
   ↓
7. Returns JSON with stats:
   {
     "total_bookings": 42,
     "pending_bookings": 8,
     "total_revenue": 125000,
     "top_destination": "Hundru Falls",
     "user_growth": [...]
   }
   ↓
8. Frontend renders charts & metrics in admin_dashboard.html
```

### **AI Chatbot Integration**
```
1. User types message in chatbot box (index.html)
   ↓
2. Frontend calls POST /api/chat with:
   {
     "messages": [
       {"role": "user", "content": "Tell me about waterfalls"}
     ]
   }
   ↓
3. routes.py receives request, validates ANTHROPIC_API_KEY
   ↓
4. Calls Anthropic Claude API with system prompt
   ↓
5. API returns AI response
   ↓
6. calls ChatService.save_chat_message(user_id, 'user', message)
   ↓
7. Saves to ChatHistory model in database
   ↓
8. Returns AI response to frontend
   ↓
9. Frontend displays response in chatbot window
   ↓
10. User session's chat history stored in ChatHistory records
```

---

## Key Interconnectivity Features

### **1. Role-Based Access Control (RBAC)**
- **Tourist**: Can search, book, review, view own bookings
- **Provider**: Can manage services, receive booking requests, view analytics
- **Admin**: Full access to all data, user management, approval workflows

```python
# Enforced via @login_required decorator and role checks
if session['user']['role'] != 'admin':
    return {"error": "Unauthorized"}, 403
```

### **2. Data Consistency Through ORM**
- Foreign key constraints prevent orphaned records
- Cascade delete removes related records automatically
- Relationships ensure referential integrity

### **3. Auto-Calculated Fields**
- Reviews automatically recalculate destination/service ratings
- Booking status updates trigger notifications
- Chat history persisted asynchronously

### **4. Session Management**
- User credentials stored in Flask session
- SessionStorage (frontend) maintains local state
- Logout clears both server session and client storage

### **5. RESTful API Design**
- Clear resource-based URL structure
- Proper HTTP methods (GET/POST/PUT/DELETE)
- Consistent JSON response format
- Error handling with appropriate status codes

---

## Database Schema Relationships

```sql
-- Users (Core Account)
User (id, name, email, password_hash, phone, role, verified, bio)
  │
  ├─ ONE-TO-MANY → Bookings
  ├─ ONE-TO-MANY → Reviews
  ├─ ONE-TO-MANY → ChatHistory
  └─ ONE-TO-MANY → Services (as provider)

-- Destinations (Tourism Attractions)
Destination (id, name, category, description, location, lat, lon, rating)
  │
  ├─ ONE-TO-MANY → Services
  ├─ ONE-TO-MANY → Bookings
  └─ ONE-TO-MANY → Reviews

-- Services (Provider Offerings)
Service (id, provider_id, destination_id, name, service_type, price, rating)
  │
  ├─ MANY-TO-ONE → User (provider)
  ├─ MANY-TO-ONE → Destination
  ├─ ONE-TO-MANY → Bookings
  └─ ONE-TO-MANY → Reviews

-- Bookings (Purchase Records)
Booking (id, user_id, destination_id, service_id, dates, guests, total_price, status)
  │
  ├─ MANY-TO-ONE → User
  ├─ MANY-TO-ONE → Destination
  ├─ MANY-TO-ONE → Service
  └─ ONE-TO-MANY → Reviews

-- Reviews (User Feedback)
Review (id, user_id, destination_id, service_id, rating, comment)
  ├─ MANY-TO-ONE → User
  ├─ MANY-TO-ONE → Destination
  └─ MANY-TO-ONE → Service

-- Chat History (AI Conversations)
ChatHistory (id, user_id, role, content, created_at)
  └─ MANY-TO-ONE → User
```

---

## Configuration & Environment

### **.env Variables**
```
ANTHROPIC_API_KEY=sk-ant-...        # Claude AI API
FLASK_ENV=development               # Flask mode
SECRET_KEY=your-secret-key         # Session secret
HOST=127.0.0.1                     # Server host
PORT=5000                          # Server port
DATABASE_PATH=database.db          # SQLite path
```

### **Flask Configuration**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')
```

---

## API Response Format

All endpoints follow consistent JSON response structure:

### **Success Response**
```json
{
  "status": "success",
  "data": { /* endpoint-specific data */ }
}
```

### **Error Response**
```json
{
  "status": "fail",
  "message": "Error description"
}
```

### **List Response**
```json
{
  "status": "success",
  "data": [
    { "id": 1, "name": "Hundru Falls", ... },
    { "id": 2, "name": "Dassam Falls", ... }
  ],
  "total": 2
}
```

---

## Testing the Interconnectivity

### **Step 1: User Registration**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Tourist",
    "email": "john@example.com",
    "password": "Password123!",
    "role": "tourist"
  }'
```

### **Step 2: User Login**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Password123!",
    "role": "tourist"
  }'
```

### **Step 3: Get Destinations**
```bash
curl http://localhost:5000/api/destinations
```

### **Step 4: Create Booking**
```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": 1,
    "service_id": 1,
    "dates": ["2024-12-20", "2024-12-22"],
    "guests": 2
  }'
```

### **Step 5: Submit Review**
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": 1,
    "service_id": 1,
    "rating": 5,
    "comment": "Amazing experience!"
  }'
```

---

## Deployment Checklist

- [ ] Create `.env` file with production keys
- [ ] Set `FLASK_ENV=production`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up Anthropic API key
- [ ] Initialize database with `db.create_all()`
- [ ] Add seed data (destinations, sample users)
- [ ] Configure CORS for frontend domain
- [ ] Set up HTTPS/SSL
- [ ] Configure logging & monitoring
- [ ] Test all API endpoints
- [ ] Perform load testing
- [ ] Set up automated backups

---

## Summary

The Jharkhand Tourism platform implements a complete **three-tier architecture** with:

✅ **Data Layer**: SQLAlchemy ORM with proper relationships  
✅ **Business Logic Layer**: Service classes with validation  
✅ **API Layer**: RESTful endpoints with role-based access  
✅ **Presentation Layer**: Interactive HTML/JS frontend  

All components are **interconnected** through:
- Session-based authentication
- Foreign key relationships
- Service layer integration
- Consistent API contracts
- Frontend form submissions

This ensures a **seamless, secure, and scalable** platform for Jharkhand tourism!
