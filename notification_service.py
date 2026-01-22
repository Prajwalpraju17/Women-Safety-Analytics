import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    def __init__(self):
        self.whatsapp_api_url = "https://api.whatsapp.com/send"
        
    def send_sms(self, phone_number, message):
        # Simulate SMS sending (integrate with Twilio/AWS SNS in production)
        print(f"SMS sent to {phone_number}: {message}")
        return True
    
    def send_whatsapp(self, phone_number, message):
        # WhatsApp Business API integration
        whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
        print(f"WhatsApp message sent to {phone_number}: {whatsapp_url}")
        return whatsapp_url
    
    def send_email(self, email, subject, message):
        try:
            # Gmail SMTP configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = "safety.alert@womensafety.com"
            msg['To'] = email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Simulate email sending
            print(f"Email sent to {email}: {subject}")
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_emergency_alerts(self, user_data, location):
        alerts_sent = []
        
        # Emergency message with location
        message = f"🚨 EMERGENCY ALERT 🚨\n\nUser {user_data['user_id']} needs immediate help!\n\nLocation: https://maps.google.com/maps?q={location['latitude']},{location['longitude']}\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nPlease contact them immediately or call emergency services."
        
        # Send to all emergency contacts
        for contact in user_data.get('emergency_contacts', []):
            if '@' in contact:  # Email
                self.send_email(contact, "🚨 EMERGENCY ALERT", message)
                alerts_sent.append(f"Email: {contact}")
            else:  # Phone number
                self.send_sms(contact, message)
                whatsapp_url = self.send_whatsapp(contact, message)
                alerts_sent.append(f"SMS/WhatsApp: {contact}")
        
        return alerts_sent