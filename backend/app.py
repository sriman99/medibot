import os
import logging
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from database import MedicalHistoryDB  # Changed from relative import to direct import

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API key is missing. Please set GEMINI_API_KEY in the .env file.")

# Initialize LangChain with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Initialize Flask app and database
app = Flask(__name__)
CORS(app)
db = MedicalHistoryDB()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LangChain prompt templates
CHAT_PROMPT = PromptTemplate(
    input_variables=["context", "user_name", "query"],
    template="""
    Context: {context}
    User {user_name} asks: {query}
    Please provide medical information and recommendations.
    """
)

WELLNESS_PROMPT = PromptTemplate(
    input_variables=["user_name", "age", "gender", "lifestyle", "goals"],
    template="""
    Create a comprehensive wellness plan for:
    Name: {user_name}
    Age: {age}
    Gender: {gender}
    Lifestyle: {lifestyle}
    Goals: {goals}
    
    Include:
    1. Diet recommendations
    2. Exercise routine
    3. Lifestyle modifications
    4. Progress tracking metrics
    5. Weekly goals
    """
)

SYMPTOM_PROMPT = PromptTemplate(
    input_variables=["symptoms"],
    template="""
    Analyze these symptoms: {symptoms}
    
    Provide:
    1. Possible conditions
    2. Severity assessment
    3. Recommended actions
    4. Red flags to watch for
    5. When to seek immediate medical attention
    """
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get('user_id', str(uuid.uuid4()))
        user_name = data['user_name']
        query = data['query']

        # Get user's medical history for context
        history = db.get_user_history(user_id)
        context = "Previous Medical History:\n"
        for date, symptoms, summary, _ in history:
            context += f"Date: {date}\nSymptoms: {symptoms}\nSummary: {summary}\n\n"

        # Create LangChain chain for chat
        chat_chain = LLMChain(llm=llm, prompt=CHAT_PROMPT)
        
        # Generate response
        response = chat_chain.run(
            context=context,
            user_name=user_name,
            query=query
        )

        if not response:
            return jsonify({"error": "Failed to generate response"}), 500

        # Create summary chain
        summary_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["text"],
                template="Summarize this medical interaction: {text}"
            )
        )
        
        # Generate summary
        summary = summary_chain.run(text=query)
        
        # Extract symptoms
        symptom_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["text"],
                template="Extract symptoms from this text: {text}"
            )
        )
        symptoms = symptom_chain.run(text=query)

        # Save to database
        db.add_medical_history(
            user_id=user_id,
            symptoms=symptoms or "No symptoms mentioned",
            chat_summary=summary or "No summary available",
            ai_recommendations=response
        )

        return jsonify({
            "answer": response,
            "timestamp": str(datetime.now())
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/generate_wellness_plan', methods=['POST'])
def wellness_plan():
    try:
        data = request.json
        wellness_chain = LLMChain(llm=llm, prompt=WELLNESS_PROMPT)
        
        response = wellness_chain.run(
            user_name=data['user_name'],
            age=data['age'],
            gender=data['gender'],
            lifestyle=data['lifestyle'],
            goals=data['goals']
        )

        if not response:
            return jsonify({"error": "Failed to generate wellness plan"}), 500

        return jsonify({
            "wellness_plan": {
                "plan": {"text": response},
                "created_at": str(datetime.now())
            }
        })
    except Exception as e:
        logger.error(f"Error in wellness_plan endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/symptom_checker', methods=['POST'])
def symptom_checker():
    try:
        symptoms = request.json.get('symptoms', '')
        symptom_chain = LLMChain(llm=llm, prompt=SYMPTOM_PROMPT)
        
        response = symptom_chain.run(symptoms=symptoms)
        
        if not response:
            return jsonify({"error": "Failed to analyze symptoms"}), 500

        return jsonify({
            "response": {
                "text": response
            }
        })
    except Exception as e:
        logger.error(f"Error in symptom_checker endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health_resources', methods=['POST'])
def health_resources():
    try:
        location = request.json.get('location', '')
        resource_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["location"],
                template="""
                Find health and wellness resources in {location}:
                
                Include:
                1. Hospitals and clinics
                2. Emergency services
                3. Pharmacies
                4. Mental health services
                5. Wellness centers
                """
            )
        )
        
        response = resource_chain.run(location=location)
        
        if not response:
            return jsonify({"error": "Failed to find resources"}), 500

        return jsonify({
            "resources": {
                "resources": {"text": response}
            }
        })
    except Exception as e:
        logger.error(f"Error in health_resources endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/medication', methods=['POST'])
def medication():
    try:
        condition = request.json.get('condition', '')
        medication_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["condition"],
                template="""
                Provide information about medications for {condition}:
                
                Include:
                1. Common medications
                2. Usage guidelines
                3. Potential side effects
                4. Drug interactions
                5. Important precautions
                """
            )
        )
        
        response = medication_chain.run(condition=condition)
        
        if not response:
            return jsonify({"error": "Failed to fetch medication data"}), 500

        return jsonify({
            "information": {
                "text": response
            }
        })
    except Exception as e:
        logger.error(f"Error in medication endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)