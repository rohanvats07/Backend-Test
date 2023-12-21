from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Mock database for demonstration purposes
users_db = {}

@app.route('/register', methods=['POST'])
def register():
    # Get registration data from the form
    email = request.form.get('email')
    
    # Generate activation token
    activation_token = str(uuid.uuid4())
    
    # Store user data and activation token in the database
    users_db[email] = {'activation_token': activation_token, 'verified': False}
    
    # Send verification email
    send_verification_email(email, activation_token)
    
    return "Registration successful. Check your email for verification instructions."

@app.route('/verify/<activation_token>')
def verify(activation_token):
    # Look up user by activation token
    for email, user_data in users_db.items():
        if user_data['activation_token'] == activation_token and not user_data['verified']:
            # Mark user as verified
            users_db[email]['verified'] = True
            return f"Email {email} verified successfully!"
    
    return "Invalid or expired activation token."

def send_verification_email(email, activation_token):
    # This is a simple example, and you should use a dedicated email service in production
    # Update the email configuration with your own SMTP server details
    smtp_server = 'your_smtp_server.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'
    sender_email = 'your_sender_email@example.com'
    
    # Construct the verification link
    verification_link = f'http://your_website.com/verify/{activation_token}'
    
    # Compose the email
    subject = 'Account Verification'
    body = f'Click the following link to verify your email: {verification_link}'
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = email
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [email], message.as_string())

if __name__ == '__main__':
    app.run(debug=True)
