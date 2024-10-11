from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pymysql import IntegrityError
import random

app = Flask(__name__)
CORS(app)

# connect database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4923@localhost/google_acc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'user'  # Link to the existing user table
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique = True)
    
# Define the Admin model
class Admin(db.Model):
    __tablename__ = 'admin'  # Link to the existing admin table
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key to the user table
    role = db.Column(db.String(20), nullable=False)

# Check if the user is an admin (helper function)
def is_admin(user_id):
    return Admin.query.filter_by(user_id=user_id).first() is not None


# Endpoint to test the API is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API is running'})

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    # Get login credentials from request body
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()
    
    if user:
        # Compare the entered password with the stored password
        if password == user.password:  # Replace this with `check_password_hash` if passwords are hashed
            return jsonify({'message': 'Login successful', 'user_id': user.user_id, 'username': user.username}), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    # Get registration data from request body
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Check for empty fields
    if not username or not password or not email:
        return jsonify({'message': 'Please fill in all fields'}), 400
    
    # Generate custom ID
    random_part = str(random.randint(1000, 9999))  # 4-digit random number
    username_part = username[:3].lower()  # First 3 letters of username
    custom_id = f"{random_part}{username_part}"

    # Create a new User instance
    new_user = User(user_id=custom_id, username=username, password=password, email=email)

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except IntegrityError:
        # Rollback the session in case of an IntegrityError (unique constraint violation)
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 409
    
# Check if the user is an admin
@app.route('/check_admin', methods=['POST'])
def check_admin():
    data = request.json
    user_id = data.get('user_id')

    # Query the Admin table to check if the user_id exists
    admin = Admin.query.filter_by(user_id=user_id).first()

    if admin:
        return jsonify({'is_admin': True, 'role': admin.role}), 200
    else:
        return jsonify({'is_admin': False}), 200
    


# Admin endpoint to show basic details of all users
@app.route('/get_users', methods=['POST'])
def get_users():
    data = request.json
    user_id = data.get('user_id')

    # Check if the requesting user is an admin
    if not is_admin(user_id):
        return jsonify({'message': 'Access denied: Admins only'}), 403

    # Query all users from the user table
    users = User.query.all()
    user_list = [{'user_id': user.user_id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify({'users': user_list}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)