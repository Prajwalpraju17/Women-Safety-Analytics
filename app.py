from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

# In-memory user storage (use database in production)
users_db = {}

@app.route('/api/google-login', methods=['POST'])
def google_login():
    data = request.json
    google_token = data.get('google_token')
    user_email = data.get('email')
    user_name = data.get('name')
    
    # Verify Google token (integrate with Google OAuth in production)
    user_id = user_email.split('@')[0]
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'email': user_email,
        'name': user_name
    })

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('user_id')
    phone = data.get('phone')
    email = data.get('email', '')
    emergency_contacts = data.get('emergency_contacts', [])
    
    print(f"Registering user: {user_id}")
    print(f"Phone: {phone}")
    print(f"Email: {email}")
    print(f"Emergency contacts: {emergency_contacts}")
    
    users_db[user_id] = {
        'phone': phone,
        'email': email,
        'emergency_contacts': emergency_contacts,
        'registered_at': datetime.now().isoformat()
    }
    
    print(f"Users database now contains: {list(users_db.keys())}")
    
    return jsonify({'success': True, 'message': 'User registered successfully'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Women Safety Analytics API is running', 'status': 'active'})

@app.route('/api/test', methods=['GET', 'POST'])
def test_connection():
    return jsonify({'status': 'Backend connected successfully', 'port': 5000, 'cors': 'enabled'})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'endpoints': ['/api/threat-detection', '/api/emergency-alert']})

@app.route('/api/threat-detection', methods=['POST'])
def detect_threat():
    data = request.json
    text_input = data.get('text', '')
    
    # Basic threat detection logic
    threat_keywords = ['danger', 'help', 'emergency', 'unsafe', 'scared']
    threat_level = sum(1 for word in threat_keywords if word in text_input.lower())
    
    return jsonify({
        'threat_detected': threat_level > 0,
        'threat_level': min(threat_level, 5),
        'recommendations': get_safety_tips(threat_level)
    })

@app.route('/api/emergency-alert', methods=['POST'])
def emergency_alert():
    data = request.json
    location = data.get('location', {})
    user_id = data.get('user_id')
    
    print(f"Emergency alert request for user: {user_id}")
    print(f"Available users in database: {list(users_db.keys())}")
    
    # Get user's emergency contacts
    user = users_db.get(user_id)
    if user:
        print(f"User found: {user}")
        emergency_contacts = user.get('emergency_contacts', [])
        
        # Create Google Maps link
        maps_link = f"https://maps.google.com/maps?q={location.get('latitude', 0)},{location.get('longitude', 0)}"
        
        # Simulate sending alerts
        alert_message = f"🚨 EMERGENCY ALERT 🚨\n\nUser {user_id} needs immediate help!\n\nLocation: {maps_link}\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nPlease contact them immediately or call emergency services."
        
        sent_to = []
        for contact in emergency_contacts:
            if '@' in contact:  # Email
                print(f"Email sent to {contact}: {alert_message}")
                sent_to.append(f"Email: {contact}")
            else:  # Phone number
                print(f"SMS sent to {contact}: {alert_message}")
                print(f"WhatsApp sent to {contact}: {alert_message}")
                sent_to.append(f"SMS/WhatsApp: {contact}")
        
        return jsonify({
            'alert_sent': True,
            'emergency_contacts_notified': len(sent_to),
            'contacts_notified': sent_to,
            'location': location,
            'maps_link': maps_link,
            'message': f"Emergency alert sent to {len(sent_to)} contacts with live location"
        })
    else:
        print(f"User {user_id} not found in database")
        return jsonify({
            'alert_sent': False,
            'error': 'User not registered'
        })

def get_safety_tips(threat_level):
    tips = [
        "Stay in well-lit areas",
        "Keep emergency contacts ready",
        "Trust your instincts",
        "Stay aware of surroundings"
    ]
    return tips[:threat_level] if threat_level > 0 else ["You're in a safe area"]

if __name__ == '__main__':
    print("Starting Women Safety Analytics Backend...")
    print("Backend will run on: http://localhost:5000")
    print("Also accessible at: http://127.0.0.1:5000")
    print("API endpoints available:")
    print("  - GET  /")
    print("  - GET  /api/test")
    print("  - POST /api/register")
    print("  - POST /api/threat-detection")
    print("  - POST /api/emergency-alert")
    print("\nCORS enabled for all origins")
    print("\nTo test: Open http://localhost:5000 in browser")
    app.run(debug=True, port=5000, host='127.0.0.1')