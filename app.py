# app.py

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_sharing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'your-mail-server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-mail-username'
app.config['MAIL_PASSWORD'] = 'your-mail-password'


db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_operation_user = db.Column(db.Boolean, default=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('files', lazy=True))

# Custom Decorator to Check if User is an Operation User
def operation_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user and g.user.is_operation_user:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Operation User Required"}), 401
    return decorated_function

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Flask-Security
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Routes

# Route to render the login page
@app.route('/login', methods=['GET'])
def render_login():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            response = jsonify({"message": "Login successful"})
            response.set_cookie('user_id', str(user.id))
            return response
        else:
            return jsonify({"message": "Invalid credentials"}), 401
        

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in request.cookies:
        user = User.query.filter_by(id=request.cookies.get('user_id')).first()
        g.user = user

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username, password=password).first()

#     if user:
#         response = jsonify({"message": "Login successful"})
#         response.set_cookie('user_id', str(user.id))
#         return response
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

@app.route('/upload', methods=['POST'])
@operation_user_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        user_id = g.user.id
        filename = secure_filename(file.filename)
        file_type = filename.rsplit('.', 1)[1].lower()

        if file_type in ['pptx', 'docx', 'xlsx']:
            new_file = File(filename=filename, file_type=file_type, user_id=user_id)
            db.session.add(new_file)
            db.session.commit()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify({"message": "File uploaded successfully"})
        else:
            return jsonify({"message": "Invalid file type"}), 400
    else:
        return jsonify({"message": "File type not allowed"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pptx', 'docx', 'xlsx']

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
