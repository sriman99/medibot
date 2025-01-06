import os
import logging
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

# Step 1: Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API key is missing. Please set GOOGLE_API_KEY in the .env file.")

# Step 2: Configure Gemini API using LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Model version
    temperature=0,           # Controls randomness
    max_tokens=None,         # Set a maximum token limit if needed
    timeout=None,            # Set a timeout limit if needed
    max_retries=2,           # Retry logic
    api_key=GOOGLE_API_KEY   # API key for Google Gemini
)

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Step 3: Define LangChain Prompt Templates

# Define the medical assistant prompt
medical_chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a medical information assistant. Please respond to the following query."),
        ("human", "{user_name} asks: {query}"),
    ]
)

# Set up LangChain LLMChain for medical queries
llm_chain = medical_chat_prompt | llm

# Step 4: Helper Functions Using LangChain

def handle_chat_query(user_id, user_name, query):
    try:
        response = llm_chain.invoke({"user_name": user_name, "query": query})
        return {
            "answer": str(response),
            "timestamp": str(datetime.now()),
            "user_id": user_id,
            "session_id": str(uuid.uuid4())
        }
    except Exception as e:
        logging.error(f"Error in handle_chat_query: {str(e)}")
        return {
            "error": "An error occurred while processing your query. Please try again.",
            "timestamp": str(datetime.now()),
            "user_id": user_id
        }

def generate_wellness_plan(user_name, age, gender, lifestyle, goals):
    try:
        wellness_plan_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Create a personalized wellness plan with the following details:"),
                ("human", "Name: {user_name}, Age: {age}, Gender: {gender}, Lifestyle: {lifestyle}, Goals: {goals}")
            ]
        )
        wellness_chain = LLMChain(llm=llm, prompt=wellness_plan_prompt)
        response = wellness_chain.invoke({
            "user_name": user_name, 
            "age": age, 
            "gender": gender, 
            "lifestyle": lifestyle, 
            "goals": goals
        })
        return {
            "plan": response,
            "user_name": user_name,
            "created_at": str(datetime.now())
        }
    except Exception as e:
        logging.error(f"Error in generate_wellness_plan: {str(e)}")
        return {"error": "Failed to generate the wellness plan. Please try again."}

def check_symptoms(symptoms):
    try:
        symptom_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Based on the following symptoms, provide information:"),
                ("human", "Symptoms: {symptoms}")
            ]
        )
        symptom_chain = LLMChain(llm=llm, prompt=symptom_prompt)
        response = symptom_chain.invoke({"symptoms": symptoms})
        return str(response)
    except Exception as e:
        logging.error(f"Error in check_symptoms: {str(e)}")
        return "Unable to analyze symptoms at the moment. Please try again later."

def find_health_resources(location):
    try:
        resource_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Find health and wellness resources in {location}:"),
                ("human", "Location: {location}")
            ]
        )
        resource_chain = LLMChain(llm=llm, prompt=resource_prompt)
        response = resource_chain.invoke({"location": location})
        return {
            "resources": response,
            "location": location,
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        logging.error(f"Error in find_health_resources: {str(e)}")
        return []

def fetch_medication_data(condition):
    try:
        medication_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "For the condition '{condition}', provide medication details."),
                ("human", "Condition: {condition}")
            ]
        )
        medication_chain = LLMChain(llm=llm, prompt=medication_prompt)
        response = medication_chain.invoke({"condition": condition})
        return {
            "condition": condition,
            "information": response,
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        logging.error(f"Error in fetch_medication_data: {str(e)}")
        return {"error": "An unexpected error occurred while fetching medication data."}

# Step 5: API Routes

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', str(uuid.uuid4()))
    user_name = data['user_name']
    query = data['query']

    response = handle_chat_query(user_id, user_name, query)
    return jsonify(response)

@app.route('/generate_wellness_plan', methods=['POST'])
def wellness_plan():
    data = request.json
    user_name = data['user_name']
    age = data['age']
    gender = data['gender']
    lifestyle = data['lifestyle']
    goals = data['goals']

    plan = generate_wellness_plan(user_name, age, gender, lifestyle, goals)
    return jsonify({"wellness_plan": plan})

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
    return jsonify({"resources": resources})

@app.route('/medication', methods=['POST'])
def medication():
    try:
        data = request.json
        condition = data.get('condition', '').strip()
        if not condition:
            return jsonify({"error": "Condition is required."}), 400

        medication_data = fetch_medication_data(condition)
        if "error" in medication_data:
            return jsonify({"error": medication_data["error"]}), 500

        return jsonify(medication_data)
    except Exception as e:
        logging.error(f"Error in /medication endpoint: {str(e)}")
        return jsonify({"error": "Internal server error."}), 500

# Step 6: Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
