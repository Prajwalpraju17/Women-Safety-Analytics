import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = '';

function App() {
  const [inputText, setInputText] = useState('');
  const [threatResult, setThreatResult] = useState(null);
  const [location, setLocation] = useState(null);
  const [userId, setUserId] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [emergencyContacts, setEmergencyContacts] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);
  const [isGoogleLoggedIn, setIsGoogleLoggedIn] = useState(false);

  // Test backend connection on component mount
  useEffect(() => {
    const testBackendConnection = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/test`);
        const data = await response.json();
        console.log('Backend connection test:', data);
      } catch (error) {
        console.error('Backend connection failed:', error);
      }
    };
    
    testBackendConnection();
  }, []);

  // Check if user is already logged in
  useEffect(() => {
    const savedUser = localStorage.getItem('user_data');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUserId(userData.user_id || '');
      setEmail(userData.email || '');
      setPhone(userData.phone || '');
      setEmergencyContacts(userData.emergency_contacts ? userData.emergency_contacts.join(', ') : '');
      setIsRegistered(userData.registered || false);
    }
  }, []);

  const googleLogin = () => {
    // Simulate Google OAuth (integrate with Google Sign-In in production)
    const mockGoogleUser = {
      email: 'user@gmail.com',
      name: 'User Name',
      user_id: 'user_gmail'
    };
    
    setUserId(mockGoogleUser.user_id);
    setEmail(mockGoogleUser.email);
    
    localStorage.setItem('user_data', JSON.stringify(mockGoogleUser));
    alert('Google login successful! Please complete registration.');
  };

  const registerUser = async () => {
    if (!userId || !phone || !email) {
      alert('Please fill in all required fields');
      return;
    }
    
    const contacts = emergencyContacts.split(',').map(c => c.trim()).filter(c => c);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/register`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          user_id: userId, 
          phone: phone,
          email: email,
          emergency_contacts: contacts 
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      if (result.success) {
        setIsRegistered(true);
        const userData = {
          user_id: userId,
          email: email,
          phone: phone,
          emergency_contacts: contacts,
          registered: true
        };
        localStorage.setItem('user_data', JSON.stringify(userData));
        alert('Registration successful! Emergency contacts will receive SMS, WhatsApp, and Email alerts.');
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert('Backend server not running. Please start the backend first.');
    }
  };

  const analyzeText = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/threat-detection`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setThreatResult(result);
    } catch (error) {
      console.error('Error:', error);
      alert('Backend server not running. Please start the backend first.');
    }
  };

  const sendEmergencyAlert = async () => {
    if (!isRegistered || !userId) {
      alert('Please register first to use emergency alerts');
      return;
    }
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const loc = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };
        setLocation(loc);
        
        console.log('Sending emergency alert for user:', userId); // Debug log
        
        try {
          const response = await fetch(`${API_BASE_URL}/api/emergency-alert`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            body: JSON.stringify({ location: loc, user_id: userId })
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const result = await response.json();
          console.log('Emergency alert result:', result); // Debug log
          
          if (result.alert_sent) {
            alert(`🚨 EMERGENCY ALERT SENT! 🚨\n\n✅ ${result.emergency_contacts_notified} contacts notified via SMS, WhatsApp & Email\n📍 Live location shared: ${result.maps_link}`);
            
            // Open Google Maps link
            window.open(result.maps_link, '_blank');
          } else {
            alert('Failed to send alert: ' + result.error);
          }
        } catch (error) {
          console.error('Emergency alert error:', error);
          alert('Backend server not running. Please start the backend first.');
        }
      });
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ Women Safety Analytics</h1>
      </header>
        
      {!isRegistered && (
        <div>
          <div className="login-section">
            <h2>🔐 Quick Login Options</h2>
            <button className="btn-google" onClick={googleLogin}>
              🔑 Sign in with Google
            </button>
            <p style={{margin: '10px 0', color: '#6c757d', fontSize: '14px'}}>Or register manually below</p>
          </div>
          
          <div className="registration">
            <h2>📱 Register for Emergency Alerts</h2>
            <input
              type="email"
              placeholder="✉️ Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="text"
              placeholder="👤 User ID"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
            <input
              type="tel"
              placeholder="📞 Your Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
            <input
              type="text"
              placeholder="🚨 Emergency Contacts (phone/email, comma separated)"
              value={emergencyContacts}
              onChange={(e) => setEmergencyContacts(e.target.value)}
            />
            <button className="btn-primary" onClick={registerUser}>Complete Registration</button>
          </div>
        </div>
      )}
      
      {isRegistered && (
        <div>
          <div className="user-info">
            <p>✅ Registered: {email}</p>
            <p>📞 Phone: {phone}</p>
            <button className="btn-reset" onClick={() => {
              localStorage.removeItem('user_data');
              setIsRegistered(false);
              setEmail('');
              setUserId('');
              setPhone('');
              setEmergencyContacts('');
            }}>🔄 Reset Registration</button>
          </div>
          
          <div className="threat-detection">
            <h2>🔍 Threat Detection</h2>
            <textarea
              className="threat-input"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Describe your situation or surroundings..."
              rows="4"
            />
            <button className="btn-analyze" onClick={analyzeText}>Analyze Threat</button>
            
            {threatResult && (
              <div className="result">
                <div className={`threat-level ${threatResult.threat_detected ? 'threat-detected' : 'threat-safe'}`}>
                  Threat Level: {threatResult.threat_level}/5
                </div>
                <p className={threatResult.threat_detected ? 'threat-detected' : 'threat-safe'}>
                  Status: {threatResult.threat_detected ? '⚠️ THREAT DETECTED' : '✅ SAFE'}
                </p>
                <div className="safety-tips">
                  <h3>💡 Safety Tips:</h3>
                  <ul>
                    {threatResult.recommendations.map((tip, index) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>

          <div className="emergency-section">
            <button className="emergency-btn" onClick={sendEmergencyAlert}>
              🚨 EMERGENCY ALERT
            </button>
            {location && (
              <div className="location-info">
                📍 Location: {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;