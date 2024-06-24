from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

def calculate_protein_intake(weight, activity_level, age, gender):
    basic_protein = 0.8 * weight
    activity_multiplier = float(activity_level)

    protein_for_activity = basic_protein * activity_multiplier
    gender_adjustment = 1.1 if gender == "1" else 1.0
    age_adjustment = 1.2 if int(age) > 50 else 1.0
    total_protein_intake = protein_for_activity * gender_adjustment * age_adjustment
    return round(total_protein_intake, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    weight = float(data['weight'])
    activity = data['activity']
    age = data['age']
    gender = data['gender']
    
    protein_intake = calculate_protein_intake(weight, activity, age, gender)
    
    return jsonify({'protein_intake': protein_intake})

if __name__ == '__main__':
    app.run(debug=True)
