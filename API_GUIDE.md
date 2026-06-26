# Jharkhand Tourism - API Documentation

## 📡 Available Endpoints

### Base URL
```
http://127.0.0.1:5000
```

---

## 🏠 Home Page

### GET /
Returns the main tourism guide page.

**Response:** HTML page

**Example:**
```bash
curl http://127.0.0.1:5000/
```

---

## 💬 Chat Endpoint (Chatbot)

### POST /chat
Send a message to the Jharkhand AI Travel Guide.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What are the best waterfalls in Jharkhand?"
}
```

**Response:**
```json
{
  "reply": "Jharkhand is famous for its stunning waterfalls...",
  "status": "success"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Tell me about Hundru Falls\"}"
```

---

## 👤 User Endpoints

### POST /register
Create a new user account.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response (Success):**
```json
{
  "message": "Registration successful",
  "status": "success"
}
```

**Response (Error):**
```json
{
  "message": "Email already exists",
  "status": "error"
}
```

---

### POST /login
Login to user account.

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response (Success):**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "status": "success"
}
```

---

### GET /logout
Logout current user session.

**Response:**
```json
{
  "message": "Logged out successfully",
  "status": "success"
}
```

---

## 🎫 Booking Endpoints

### POST /book
Create a new booking.

**Request:**
```json
{
  "destination": "Hundru Falls",
  "date": "2026-06-15",
  "guests": 4,
  "notes": "Interested in guided tour"
}
```

**Response:**
```json
{
  "booking_id": 123,
  "message": "Booking created successfully",
  "status": "success"
}
```

---

### GET /bookings
Get all bookings for logged-in user.

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "destination": "Hundru Falls",
      "date": "2026-06-15",
      "guests": 4,
      "status": "confirmed"
    }
  ],
  "status": "success"
}
```

---

## 📍 Destination Endpoints

### GET /destinations
Get list of all destinations.

**Response:**
```json
{
  "destinations": [
    {
      "id": 1,
      "name": "Hundru Falls",
      "category": "Waterfall",
      "description": "Stunning 98-meter high waterfall...",
      "image": "hundru_falls.jpg"
    }
  ],
  "status": "success"
}
```

---

### GET /destinations/<id>
Get details of a specific destination.

**Response:**
```json
{
  "destination": {
    "id": 1,
    "name": "Hundru Falls",
    "description": "...",
    "location": "Ranchi",
    "best_time": "July-September",
    "ratings": 4.8
  }
}
```

---

## 🧑 Profile Endpoints

### GET /profile
Get current user profile (requires login).

**Response:**
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "tourist"
  }
}
```

---

### PUT /profile
Update user profile.

**Request:**
```json
{
  "name": "Jane Doe",
  "phone": "9876543210"
}
```

---

## ❌ Error Responses

All endpoints return errors in this format:

```json
{
  "message": "Error description",
  "status": "error"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (not logged in)
- `403` - Forbidden (permission denied)
- `404` - Not Found
- `500` - Server Error

---

## 🔒 Authentication

Some endpoints require user login. Include session cookies:

```bash
curl -c cookies.txt -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"john@example.com\", \"password\": \"pass\"}"

curl -b cookies.txt http://127.0.0.1:5000/profile
```

---

## 📝 Testing with Postman

1. Import endpoints into Postman
2. Set base URL: `http://127.0.0.1:5000`
3. For POST requests, set Header: `Content-Type: application/json`
4. Paste JSON in Body section (raw format)

---

## 🚀 Rate Limiting

No rate limiting currently implemented. Implement cautiously for production.

---

## 📞 Support

For issues with API endpoints, check:
- Application console for error messages
- `SETUP.md` for configuration
- `README.md` for project overview
