from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import os

# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase/protien-6103b-firebase-adminsdk-jyocv-406e47ea69.json')
firebase_admin.initialize_app(cred)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, uid, email):
        self.id = uid
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user_info = session.get('user_info')
    if user_info:
        return User(user_info['uid'], user_info['email'])
    return None

def calculate_protein_intake(weight, activity_level, age, gender):
    basic_protein = 0.8 * weight
    activity_multiplier = float(activity_level)
    protein_for_activity = basic_protein * activity_multiplier
    gender_adjustment = 1.1 if gender == "1" else 1.0
    age_adjustment = 1.2 if int(age) > 50 else 1.0
    total_protein_intake = protein_for_activity * gender_adjustment * age_adjustment
    return round(total_protein_intake, 2)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.get_json()
    weight = float(data['weight'])
    activity = data['activity']
    age = data['age']
    gender = data['gender']
    protein_intake = calculate_protein_intake(weight, activity, age, gender)
    return redirect(url_for('model', protein_intake=protein_intake))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = request.json.get('token')
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            session['user_info'] = {'uid': uid, 'email': email}
            login_user(User(uid, email))
            return jsonify({'message': 'Login successful'}), 200
        except exceptions.FirebaseError as e:
            return jsonify({'message': f'Error: {e}'}), 401
    return render_template('login.html')

@app.route('/model')
@login_required
def model():
    return render_template('model.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['password']
        
        # Validate the inputs (e.g., check email format, phone number validity)
        # This step is skipped for brevity but is important to implement
        
        try:
            # Create the user with Firebase Authentication
            user_record = auth.create_user(
                email=email,
                password=password,
                phone_number=phone,
                display_name=name
                # Note: Firebase Auth doesn't directly support storing gender, 
                # so you might need to use Firestore or another database for additional fields
            )
            
            # Additional step to store the gender and any other extra information in Firestore
            # This is a placeholder for storing extra data in Firestore or your chosen database
            
            # Redirect to the login page or dashboard after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            return str(e)
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_info', None)
    return redirect(url_for('landing_page'))

if __name__ == '__main__':
    app.run(debug=True)
