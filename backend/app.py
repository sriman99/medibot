import os
import logging
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import handle_chat_query
from health_report import generate_health_report
from symptom_checker import check_symptoms
from resources_finder import find_health_resources


# Step 1: Load API keys from .env file
load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

if not google_api_key or not pinecone_api_key:
    raise ValueError("API keys are missing. Please set GEMINI_API_KEY and PINECONE_API_KEY in the .env file.")

# Step 2: Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Step 3: Endpoints

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', str(uuid.uuid4()))
    user_name = data['user_name']
    query = data['query']

    response = handle_chat_query(user_id, user_name, query)
    return jsonify({"response": response})

@app.route('/generate_health_report', methods=['POST'])
def health_report():
    data = request.json
    user_name = data['user_name']
    age = data['age']
    gender = data['gender']
    medical_history = data['medical_history']
    current_medications = data['current_medications']

    report = generate_health_report(user_name, age, gender, medical_history, current_medications)
    
    return jsonify({"report": report})

@app.route('/symptom_checker', methods=['POST'])
def symptom_checker():
    data = request.json
    symptoms = data.get('symptoms', '')
    response = check_symptoms(symptoms)
    return jsonify({"response": response})

@app.route('/health_resources', methods=['POST'])
def health_resources():
    data = request.json
    location = data.get('location', '')
    resources = find_health_resources(location)
    # log_activity('health_resources', data.get('user_id', 'anonymous'), location, resources)
    return jsonify({"resources": resources})

if __name__ == '__main__':
    app.run(debug=True)
