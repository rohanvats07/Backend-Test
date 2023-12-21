from flask import Flask, request
from flaskext.mysql import MySQL
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_DATABASE_USER'] = 'your_mysql_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DATABASE_DB'] = 'mydatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')  # Make sure to hash and salt passwords in a real application
    
    activation_token = str(uuid.uuid4())
    
    # Store user data and activation token in the database
    cursor = mysql.get_db().cursor()
    cursor.execute("INSERT INTO users (email, password, activation_token) VALUES (%s, %s, %s)",
                   (email, password, activation_token))
    
    # Commit the changes to the database
    mysql.get_db().commit()
    
    send_verification_email(email, activation_token)
    
    return "Registration successful. Check your email for verification instructions."

@app.route('/verify/<activation_token>')
def verify(activation_token):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT email FROM users WHERE activation_token = %s AND verified = 0", (activation_token,))
    user = cursor.fetchone()

    if user:
        # Mark user as verified
        cursor.execute("UPDATE users SET verified = 1 WHERE email = %s", (user[0],))
        mysql.get_db().commit()
        return f"Email {user[0]} verified successfully!"

    return "Invalid or expired activation token."

# Rest of the code remains the same

if __name__ == '__main__':
    app.run(debug=True)
