from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pymysql import IntegrityError
import random
import string
from datetime import datetime

app = Flask(__name__)
CORS(app)

# connect database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4923@localhost/google_acc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'user' 
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique = True)
    
# Define the Admin model
class Admin(db.Model):
    __tablename__ = 'admin' 
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key to the user table
    role = db.Column(db.String(20), nullable=False)

# Define the Service model
class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=True)

# Define the Privilege model
class Privilege(db.Model):
    __tablename__ = 'privelage'
    privelage_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    
# Security table model
class Security(db.Model):
    __tablename__ = 'security'
    sec_id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    login_time = db.Column(db.String(50), nullable=False)



def generate_security_id():
    """Generate a random security ID with 3 random digits and 3 random uppercase letters."""
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return digits + letters

# Function to insert login details into the security table
def insert_login_security(user_id):
    # Capture current login time
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate a random security ID
    sec_id = generate_security_id()

    # Create a new security record
    new_security = Security(sec_id=sec_id, user_id=user_id, login_time=login_time)

    try:
        # Add to database and commit
        db.session.add(new_security)
        db.session.commit()
        print(f"Login record added for user {user_id} at {login_time}")
    except IntegrityError:
        db.session.rollback()
        print(f"Error inserting login record for user {user_id}")


# Check if the user is an admin (helper function)
def is_admin(user_id):
    return Admin.query.filter_by(user_id=user_id).first() is not None

def generate_service_id():
    """Generate a random user ID with 4 random digits and 4 random alphabets."""
    digits = ''.join(random.choices(string.digits, k=4))
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    return digits + letters


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
            # Call the function to insert login data into the security table
            insert_login_security(user.user_id)
            
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


# Edit user details endpoint
@app.route('/edit', methods=['PUT'])
def edit_user():
    # Get the user_id and new details from the request body
    data = request.json
    user_id = data.get('user_id')
    new_username = data.get('username')
    new_password = data.get('password')
    new_email = data.get('email')

    # Check if the user exists
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Update the fields based on the provided values
    if new_username:
        if User.query.filter_by(username=new_username).first():
            return jsonify({'message': 'Username already exists'}), 409
        user.username = new_username

    if new_password:
        user.password = new_password  # Ideally, hash the password before saving

    if new_email:
        if User.query.filter_by(email=new_email).first():
            return jsonify({'message': 'Email already exists'}), 409
        user.email = new_email

    try:
        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'User details updated successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error updating user details'}), 500


@app.route('/add_service', methods=['POST'])
def add_service():
    data = request.json
    service_name = data.get('service_name')
    url = data.get('url')

    # Check if the service already exists
    if Service.query.filter_by(service_name=service_name).first():
        return jsonify({'message': 'Service already exists'}), 409
    
    service_id = generate_service_id()

    # Create a new Service
    new_service = Service(service_id=service_id,service_name=service_name, url=url)

    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error adding service'}), 500


@app.route('/remove_service', methods=['DELETE'])
def remove_service():
    data = request.json
    service_id = data.get('service_id')

    # Find the service by ID
    service = Service.query.filter_by(service_id=service_id).first()

    if not service:
        return jsonify({'message': 'Service not found'}), 404

    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service removed successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error removing service'}), 500


@app.route('/assign_privilege', methods=['POST'])
def assign_privilege():
    data = request.json
    user_id = data.get('user_id')
    service_id = data.get('service_id')
    role = data.get('role', 'viewer')

    # Check if the user already has privileges for this service
    if Privilege.query.filter_by(user_id=user_id, service_id=service_id).first():
        return jsonify({'message': 'Privilege already assigned to this user'}), 409

    # Create a new Privilege record
    new_privilege = Privilege(user_id=user_id, service_id=service_id, role=role)

    try:
        db.session.add(new_privilege)
        db.session.commit()
        return jsonify({'message': 'Privilege assigned successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error assigning privilege'}), 500


@app.route('/get_services', methods=['POST'])
def get_services():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        privileges = Privilege.query.filter_by(user_id=user_id).all()
        

        services_list = []
        for privilege in privileges:
            service = Service.query.filter_by(service_id=privilege.service_id).first()
            if service:
                services_list.append({
                    'service_id': service.service_id,
                    'service_name': service.service_name,
                    'url': service.url,
                    'role': privilege.role
                })

        return jsonify({'services': services_list}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/services', methods=['GET'])
def services():
    services = Service.query.all()
    service_list = [{'service_id': service.service_id, 'service_name': service.service_name} for service in services]
    return jsonify({'services': service_list}), 200




# Run the app
if __name__ == '__main__':
    app.run(debug=True)