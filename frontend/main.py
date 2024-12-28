
# import streamlit as st
# import requests
# from datetime import datetime
# from dotenv import load_dotenv
# import sys
# import os

# # Add the backend directory to the Python path
# sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# # Load environment variables
# load_dotenv()

# # Streamlit page configuration
# st.set_page_config(page_title="MediBot", page_icon="🩺", layout="centered")

# # Title and description
# st.title("MediBot - Your Personal Health Assistant")
# st.write("Welcome! I am here to assist you with health-related queries.")

# # Define API URLs for backend services (replace with actual backend URLs)
# CHATBOT_API_URL = "http://localhost:5000/chat"
# SYMPTOM_CHECKER_API_URL = "http://localhost:5000/symptom_checker"
# RESOURCE_FINDER_API_URL = "http://localhost:5000/resources_finder"

# # Function to log user activity locally
# def log_user_activity(query, response):
#     with open("activity_log.txt", "a") as log_file:
#         log_file.write(f"{datetime.now()} - Query: {query} - Response: {response}\n")

# # --- Chatbot Interaction ---
# st.header("Ask a Health Question")
# with st.container():  # Use st.container() instead of st.beta_container()
#     # Create a card for the chatbot
#     with st.container():
#         card_style = """
#         <style>
#             .card {
#                 background-color: #1E293B;
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin-bottom: 20px;
#                 transition: all 0.3s ease-in-out;
#             }
#             .card:hover {
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#             }
#             .card .expanded {
#                 transform: scale(1.1);
#             }
#         </style>
#         """
#         st.markdown(card_style, unsafe_allow_html=True)
        
#         user_name = st.text_input("Enter your name:", value="default_user")  # Default to "default_user" if not entered
#         user_query = st.text_input("Enter your health-related question:")
        
#         if user_query:
#             log_user_activity(user_query, "Waiting for response...")

#             try:
#                 # Send the user query and user name to the chatbot API
#                 response = requests.post(CHATBOT_API_URL, json={"user_name": user_name, "query": user_query})
#                 chatbot_response = response.json().get("response", "Sorry, I couldn't understand that.")
#             except Exception as e:
#                 chatbot_response = "There was an error processing your request. Please try again later."
            
#             # Create an expandable card for the chatbot response
#             with st.container():
#                 card_class = "card expanded" if chatbot_response else "card"
#                 st.markdown(f"""
#                     <div class="{card_class}">
#                         <h4><strong>Chatbot Response:</strong></h4>
#                         <p>{chatbot_response}</p>
#                     </div>
#                 """, unsafe_allow_html=True)
#             log_user_activity(user_query, chatbot_response)


# # --- Symptom Checker ---
# st.header("Symptom Checker")
# with st.container():
#     # Create a card for the symptom checker
#     symptoms_input = st.text_area("Enter symptoms (separate with commas):")
    
#     if symptoms_input:
#         try:
#             # Send symptoms to the symptom checker API
#             response = requests.post(SYMPTOM_CHECKER_API_URL, json={"symptoms": symptoms_input})
#             symptom_check_result = response.json().get("result", "No conditions found.")
#         except Exception as e:
#             symptom_check_result = "There was an error processing your symptoms. Please try again later."
        
#         # Create an expandable card for the symptom check result
#         with st.container():
#             card_class = "card expanded" if symptom_check_result else "card"
#             st.markdown(f"""
#                 <div class="{card_class}">
#                     <h4><strong>Possible Conditions:</strong></h4>
#                     <p>{symptom_check_result}</p>
#                 </div>
#             """, unsafe_allow_html=True)

# # --- Resource Finder ---
# st.header("Find Health Resources")
# with st.container():
#     # Create a card for the resource finder
#     resource_query = st.text_input("Search for health resources:")
    
#     if resource_query:
#         try:
#             # Send the query to the resource finder API
#             response = requests.post(RESOURCE_FINDER_API_URL, json={"query": resource_query})
#             resource_result = response.json().get("resources", "No resources found.")
#         except Exception as e:
#             resource_result = "There was an error processing your request. Please try again later."
        
#         # Create an expandable card for the resources found
#         with st.container():
#             card_class = "card expanded" if resource_result else "card"
#             st.markdown(f"""
#                 <div class="{card_class}">
#                     <h4><strong>Resources Found:</strong></h4>
#                     <p>{resource_result}</p>
#                 </div>
#             """, unsafe_allow_html=True)

# # --- Activity Log ---
# st.header("View Activity Logs")

# if st.button("View Previous Interactions"):
#     # Display activity logs (optional: fetch from Pinecone or a database)
#     st.write("Displaying previous interactions...")
#     # For example, you can query Pinecone to fetch recent activities and display them.
#     # Implement the actual logic here to fetch and display logs from your Pinecone index or other database.


import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="MediBot", page_icon="🩺", layout="centered")

# Title and description
st.title("MediBot - Your Personal Health Assistant")
st.write("Welcome! I am here to assist you with health-related queries.")

# Define API URLs for backend services (replace with actual backend URLs)
CHATBOT_API_URL = "http://localhost:5000/chat"
SYMPTOM_CHECKER_API_URL = "http://localhost:5000/symptom_checker"
RESOURCE_FINDER_API_URL = "http://localhost:5000/resources_finder"
HEALTH_REPORT_API_URL = "http://localhost:5000/generate_health_report"

# Function to log user activity locally
def log_user_activity(query, response):
    with open("activity_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - Query: {query} - Response: {response}\n")

# --- Chatbot Interaction ---
st.header("Ask a Health Question")
with st.container():  # Use st.container() instead of st.beta_container()
    # Create a card for the chatbot
    with st.container():
        card_style = """
        <style>
            .card {
                background-color: #1E293B;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                transition: all 0.3s ease-in-out;
            }
            .card:hover {
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .card .expanded {
                transform: scale(1.1);
            }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)
        
        user_name = st.text_input("Enter your name:", value="default_user")  # Default to "default_user" if not entered
        user_query = st.text_input("Enter your health-related question:")
        
        if user_query:
            log_user_activity(user_query, "Waiting for response...")

            try:
                # Send the user query and user name to the chatbot API
                response = requests.post(CHATBOT_API_URL, json={"user_name": user_name, "query": user_query})
                chatbot_response = response.json().get("response", "Sorry, I couldn't understand that.")
            except Exception as e:
                chatbot_response = "There was an error processing your request. Please try again later."
            
            # Create an expandable card for the chatbot response
            with st.container():
                card_class = "card expanded" if chatbot_response else "card"
                st.markdown(f"""
                    <div class="{card_class}">
                        <h4><strong>Chatbot Response:</strong></h4>
                        <p>{chatbot_response}</p>
                    </div>
                """, unsafe_allow_html=True)
            log_user_activity(user_query, chatbot_response)

# --- Symptom Checker ---
st.header("Symptom Checker")
with st.container():
    # Create a card for the symptom checker
    symptoms_input = st.text_area("Enter symptoms (separate with commas):")
    
    if symptoms_input:
        try:
            # Send symptoms to the symptom checker API
            response = requests.post(SYMPTOM_CHECKER_API_URL, json={"symptoms": symptoms_input})
            symptom_check_result = response.json().get("result", "No conditions found.")
        except Exception as e:
            symptom_check_result = "There was an error processing your symptoms. Please try again later."
        
        # Create an expandable card for the symptom check result
        with st.container():
            card_class = "card expanded" if symptom_check_result else "card"
            st.markdown(f"""
                <div class="{card_class}">
                    <h4><strong>Possible Conditions:</strong></h4>
                    <p>{symptom_check_result}</p>
                </div>
            """, unsafe_allow_html=True)

# --- Resource Finder ---
st.header("Find Health Resources")
with st.container():
    # Create a card for the resource finder
    resource_query = st.text_input("Search for health resources:")
    
    if resource_query:
        try:
            # Send the query to the resource finder API
            response = requests.post(RESOURCE_FINDER_API_URL, json={"query": resource_query})
            resource_result = response.json().get("resources", "No resources found.")
        except Exception as e:
            resource_result = "There was an error processing your request. Please try again later."
        
        # Create an expandable card for the resources found
        with st.container():
            card_class = "card expanded" if resource_result else "card"
            st.markdown(f"""
                <div class="{card_class}">
                    <h4><strong>Resources Found:</strong></h4>
                    <p>{resource_result}</p>
                </div>
            """, unsafe_allow_html=True)

# --- Health Report Generation ---
st.header("Generate Health Report")
with st.container():
    # Form for generating health report
    with st.form(key='health_report_form'):
        user_name = st.text_input("Enter your name:")
        age = st.number_input("Enter your age:", min_value=0, max_value=120)
        gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
        medical_history = st.text_area("Enter your medical history:")
        current_medications = st.text_area("Enter your current medications:")

        submit_button = st.form_submit_button("Generate Report")

    if submit_button:
        # Prepare the data to send to the backend
        data = {
            "user_name": user_name,
            "age": age,
            "gender": gender,
            "medical_history": medical_history,
            "current_medications": current_medications
        }

        try:
            # Send the data to the backend API
            response = requests.post(HEALTH_REPORT_API_URL, json=data)
            health_report = response.json().get("report", "Unable to generate report. Please try again later.")
            
            # Display the health report
            with st.container():
                card_class = "card expanded" if health_report else "card"
                st.markdown(f"""
                    <div class="{card_class}">
                        <h4><strong>Generated Health Report:</strong></h4>
                        <p>{health_report}</p>
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.write("There was an error processing your request. Please try again later.")

# --- Activity Log ---
st.header("View Activity Logs")

if st.button("View Previous Interactions"):
    # Display activity logs (optional: fetch from Pinecone or a database)
    st.write("Displaying previous interactions...")
    # For example, you can query Pinecone to fetch recent activities and display them.
    # Implement the actual logic here to fetch and display logs from your Pinecone index or other database.
