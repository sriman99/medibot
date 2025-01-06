import streamlit as st
import requests

# API URL for the backend (replace with your backend URL)
API_URL = "http://127.0.0.1:5000"  # Adjust this to your backend's URL
import ast
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
    body {
        background-color: #111827;
        color: #e5e7eb;
        font-family: 'Roboto', sans-serif;
    }
    .header {
        font-size: 2rem;
        font-weight: bold;
        color: #F3F4F6;
    }
    .card {
        background-color: #1F2937;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
    }
    .input {
        background-color: #2D3748;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App title and description
st.title("AI Medical Assistant")
st.markdown("Welcome to the AI-powered Medical Assistant. Choose a feature below to get started.")

# Feature selection using a dropdown
feature = st.selectbox("Select a Feature", ["Chat with AI", "Generate Wellness Plan", "Symptom Checker", "Find Health Resources", "Medication Information"])

# 1. **Chat with AI**
if feature == "Chat with AI":
    st.header("Ask Health-Related Questions")
    user_name = st.text_input("Your Name", "John Doe")
    query = st.text_area("Your Query", "What are the symptoms of flu?")
    
    if st.button("Submit Query"):
        if query:
            payload = {"user_name": user_name, "query": query}
            response = requests.post(f"{API_URL}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("answer", "No answer received.")
                
                # Format the response for better readability
                content = ai_response.split('content="')[1].split('"')[0] 
                content = content.replace("\n\n", "\n\n")  # Ensure double line breaks
                content = content.replace("\n", "<br>")
                st.markdown(f'<div class="card">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p>Please enter a valid query.</p></div>', unsafe_allow_html=True)

# 2. **Generate Wellness Plan**
# elif feature == "Generate Wellness Plan":
#     st.header("Generate a Personalized Wellness Plan")
#     user_name = st.text_input("Your Name")
#     age = st.number_input("Your Age", min_value=0)
#     gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#     lifestyle = st.text_area("Lifestyle (e.g., Active, Sedentary, etc.)")
#     goals = st.text_area("Goals (e.g., Lose weight, Improve fitness, etc.)")
    
#     if st.button("Generate Plan"):
#         if user_name and age and gender and lifestyle and goals:
#             payload = {
#                 "user_name": user_name,
#                 "age": age,
#                 "gender": gender,
#                 "lifestyle": lifestyle,
#                 "goals": goals
#             }
#             response = requests.post(f"{API_URL}/generate_wellness_plan", json=payload)
#             if response.status_code == 200:
#                 data = response.json()
                
#                 wellness_plan_text = data.get("wellness_plan", {}).get("plan", {}).get("text", "Failed to generate wellness plan.")
#                 st.markdown(f'<div class="card"><p>{wellness_plan_text}</p></div>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
#         else:
#             st.markdown('<div class="card"><p>Please fill in all fields.</p></div>', unsafe_allow_html=True)

# 2. **Generate Wellness Plan**
elif feature == "Generate Wellness Plan":
    st.header("Generate a Personalized Wellness Plan")
    user_name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    lifestyle = st.text_area("Lifestyle (e.g., Active, Sedentary, etc.)")
    goals = st.text_area("Goals (e.g., Lose weight, Improve fitness, etc.)")
    
    if st.button("Generate Plan"):
        if user_name and age and gender and lifestyle and goals:
            payload = {
                "user_name": user_name,
                "age": age,
                "gender": gender,
                "lifestyle": lifestyle,
                "goals": goals
            }
            response = requests.post(f"{API_URL}/generate_wellness_plan", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                wellness_plan_text = data.get("wellness_plan", {}).get("plan", {}).get("text", "Failed to generate wellness plan.")
                
                # Display the wellness plan text
                st.markdown(f'<div class="card"><p>{wellness_plan_text}</p></div>', unsafe_allow_html=True)
                
                # Add a download button for the generated plan
                plan_filename = f"{user_name}_wellness_plan.txt"
                st.download_button(
                    label="Download Wellness Plan",
                    data=wellness_plan_text,
                    file_name=plan_filename,
                    mime="text/plain"
                )
            else:
                st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p>Please fill in all fields.</p></div>', unsafe_allow_html=True)


# 3. **Symptom Checker**
elif feature == "Symptom Checker":
    st.header("Check Your Symptoms")
    symptoms = st.text_area("Enter Symptoms (e.g., fever, headache, etc.)")
    
    if st.button("Check Symptoms"):
        if symptoms:
            payload = {"symptoms": symptoms}
            response = requests.post(f"{API_URL}/symptom_checker", json=payload)
            if response.status_code == 200:
                data = response.json()
                # Extract the response string
                symptom_response = data.get("response", "Unable to check symptoms.")
                
                # Parse the response string as a dictionary
                try:
                    response_dict = ast.literal_eval(symptom_response)  # Safely evaluate the string
                    symptom_text = response_dict.get('text', "No detailed response available.")
                except (ValueError, SyntaxError):
                    symptom_text = "Failed to parse the response text."

                # Display the extracted text
                st.markdown(f'<div class="card"><p>{symptom_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p>Please enter symptoms.</p></div>', unsafe_allow_html=True)


# 4. **Find Health Resources**
elif feature == "Find Health Resources":
    st.header("Find Health Resources in Your Location")
    location = st.text_input("Enter Your Location (City, Country)")
    
    if st.button("Find Resources"):
        if location:
            payload = {"location": location}
            response = requests.post(f"{API_URL}/health_resources", json=payload)
            if response.status_code == 200:
                data = response.json()
                resources_data = data.get("resources", {})
                
                # Extracting the text from the resources object
                resource_text = resources_data.get("resources", {}).get("text", "No resources found for this location.")
                
                # Display the extracted resources text
                st.markdown(f'<div class="card"><p>{resource_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p>Please enter a location.</p></div>', unsafe_allow_html=True)


# 5. **Medication Information**
elif feature == "Medication Information":
    st.header("Get Medication Information")
    condition = st.text_input("Enter Condition (e.g., Diabetes, Hypertension)")
    
    if st.button("Get Medication Info"):
        if condition:
            payload = {"condition": condition}
            response = requests.post(f"{API_URL}/medication", json=payload)
            if response.status_code == 200:
                data = response.json()
                medication_info = data.get("information", {}).get("text", "No information available.")
                
                # Display the extracted medication information
                st.markdown(f'<div class="card"><p>{medication_info}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card"><p>Error: Backend server is down.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><p>Please enter a condition.</p></div>', unsafe_allow_html=True)


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p class="text-center">Made By Sriman</p>', unsafe_allow_html=True)
