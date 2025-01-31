import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import json
from datetime import datetime, timedelta

# API URL for the backend
API_URL = "http://127.0.0.1:5000"

# # Configure page
# st.set_page_config(
#     page_title="AI Medical Assistant",
#     page_icon="🏥",
#     layout="wide"
# )

# Custom CSS
# Configure page with custom theme and styling
st.set_page_config(
    page_title="AI Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and modern styling
st.markdown("""
<style>
    /* Main Styling */
    .main {
        background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
        padding: 2rem;
    }
    
    /* Card Animations and Styling */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background-color: white;
        border: 2px solid #e0e6ed;
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Card Design */
    .response-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
        border: 1px solid #e0e6ed;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .response-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
        border-right: 1px solid #e0e6ed;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8f9fa;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Apply animations to elements */
    .stMarkdown, .element-container {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .sidebar .element-container {
        animation: slideIn 0.5s ease-out forwards;
    }
    
    /* Custom Components */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
        border: 1px solid #e0e6ed;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Status Indicators */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-active {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .status-pending {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    /* Map Container */
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Loading Animation */
    @keyframes loading {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading {
        width: 2rem;
        height: 2rem;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #4CAF50;
        border-radius: 50%;
        animation: loading 1s linear infinite;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 5px 10px;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_feature' not in st.session_state:
    st.session_state.current_feature = "Chat with AI"

def get_location_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="medical_assistant")
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        return None
    except GeocoderTimedOut:
        return None

def create_map_with_hospitals(location):
    # Get coordinates for the entered location
    coordinates = get_location_coordinates(location)
    if not coordinates:
        st.error("Could not find the specified location. Please try a different location.")
        return None
    
    # Create a map centered on the location
    m = folium.Map(location=coordinates, zoom_start=13)
    
    # Add a marker for the entered location
    folium.Marker(
        coordinates,
        popup="Your Location",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # In a real application, you would fetch actual hospital data from an API
    # For demonstration, we'll add some sample hospitals around the location
    sample_hospitals = [
        {"name": "General Hospital", "lat": coordinates[0] + 0.01, "lon": coordinates[1] + 0.01},
        {"name": "City Medical Center", "lat": coordinates[0] - 0.01, "lon": coordinates[1] - 0.01},
        {"name": "Community Hospital", "lat": coordinates[0] + 0.01, "lon": coordinates[1] - 0.01},
        {"name": "Emergency Care Center", "lat": coordinates[0] - 0.01, "lon": coordinates[1] + 0.01},
    ]
    
    # Add hospital markers
    for hospital in sample_hospitals:
        folium.Marker(
            [hospital["lat"], hospital["lon"]],
            popup=hospital["name"],
            icon=folium.Icon(color='blue', icon='plus', prefix='fa')
        ).add_to(m)
    
    return m

# Sidebar navigation
with st.sidebar:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    st.title("🏥 Navigation")
    st.markdown("---")
    
    if st.button("💬 Chat with AI"):
        st.session_state.current_feature = "Chat with AI"
    if st.button("🎯 Generate Wellness Plan"):
        st.session_state.current_feature = "Generate Wellness Plan"
    if st.button("🔍 Symptom Checker"):
        st.session_state.current_feature = "Symptom Checker"
    if st.button("🏥 Find Health Resources"):
        st.session_state.current_feature = "Find Health Resources"
    if st.button("💊 Medication Information"):
        st.session_state.current_feature = "Medication Information"
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main content area
st.title("🏥 AI Medical Assistant")
st.markdown("---")

# Display current feature content
if st.session_state.current_feature == "Chat with AI":
    st.header("💬 Chat with AI")
    
    # Chat history display
    for message in st.session_state.chat_history:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")
    
    # Chat input
    with st.form("chat_form"):
        user_input = st.text_area("Your message:", height=100)
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            try:
                response = requests.post(f"{API_URL}/chat", json={
                    "user_id": st.session_state.user_id,
                    "user_name": "User",
                    "query": user_input
                })
                
                if response.status_code == 200:
                    ai_response = response.json()["answer"]
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                else:
                    st.error("Failed to get response from AI")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif st.session_state.current_feature == "Generate Wellness Plan":
    st.header("🎯 Generate Wellness Plan")
    
    with st.form("wellness_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name")
            age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            lifestyle = st.selectbox("Lifestyle", ["Sedentary", "Moderately Active", "Active", "Very Active"])
        
        goals = st.text_area("Your Health Goals")
        submitted = st.form_submit_button("Generate Plan")
        
        if submitted and name and age and goals:
            try:
                response = requests.post(f"{API_URL}/generate_wellness_plan", json={
                    "user_name": name,
                    "age": age,
                    "gender": gender,
                    "lifestyle": lifestyle,
                    "goals": goals
                })
                
                if response.status_code == 200:
                    plan = response.json()["wellness_plan"]["plan"]["text"]
                    st.markdown(f'<div class="response-card">{plan}</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        "Download Plan",
                        plan,
                        file_name=f"wellness_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Failed to generate wellness plan")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif st.session_state.current_feature == "Symptom Checker":
    st.header("🔍 Symptom Checker")
    
    with st.form("symptom_form"):
        symptoms = st.text_area("Describe your symptoms in detail:")
        submitted = st.form_submit_button("Check Symptoms")
        
        if submitted and symptoms:
            try:
                response = requests.post(f"{API_URL}/symptom_checker", json={"symptoms": symptoms})
                
                if response.status_code == 200:
                    analysis = response.json()["response"]["text"]
                    st.markdown(f'<div class="response-card">{analysis}</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to analyze symptoms")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif st.session_state.current_feature == "Find Health Resources":
    st.header("🏥 Find Health Resources")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("resources_form"):
            location = st.text_input("Enter your location (City, Country)")
            submitted = st.form_submit_button("Find Resources")
            
            if submitted and location:
                try:
                    # Get AI-generated resources
                    response = requests.post(f"{API_URL}/health_resources", json={"location": location})
                    
                    if response.status_code == 200:
                        resources = response.json()["resources"]["resources"]["text"]
                        st.markdown(f'<div class="response-card">{resources}</div>', unsafe_allow_html=True)
                        
                        # Create and display the map
                        st.markdown("### 🗺️ Nearby Hospitals")
                        map_data = create_map_with_hospitals(location)
                        if map_data:
                            st.markdown('<div class="map-container">', unsafe_allow_html=True)
                            folium_static(map_data)
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Failed to find health resources")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### 📋 Quick Tips")
        st.markdown("""
        - Use specific location names
        - Include city and country
        - Check the map for nearby hospitals
        - Save important contact numbers
        - Note emergency room locations
        """)

elif st.session_state.current_feature == "Medication Information":
    st.header("💊 Medication Information")
    
    # Initialize session state for medication features
    if 'medications' not in st.session_state:
        st.session_state.medications = []
    if 'reminders' not in st.session_state:
        st.session_state.reminders = []
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []
    
    # Create tabs for different features
    tabs = st.tabs([
        "🔍 Search & Information",
        "💊 My Medications",
        "⏰ Reminders",
        "📊 Symptoms Tracker",
        "🤖 AI Assistant"
    ])
    
    # Tab 1: Search & Information
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Search Medication")
            with st.form("medication_search_form"):
                search_type = st.radio(
                    "Search by:",
                    ["Name", "Condition", "Voice Search", "Image Upload"]
                )
                
                if search_type in ["Name", "Condition"]:
                    query = st.text_input(f"Enter medication {search_type.lower()}:")
                elif search_type == "Voice Search":
                    st.info("🎤 Click to start voice recording (Feature coming soon)")
                    query = st.text_input("Or type manually:")
                else:
                    st.file_uploader("Upload medication image", type=["jpg", "png"])
                    query = st.text_input("Or type manually:")
                
                submitted = st.form_submit_button("Search")
                
                if submitted and query:
                    try:
                        response = requests.post(f"{API_URL}/medication", json={"condition": query})
                        
                        if response.status_code == 200:
                            info = response.json()["information"]["text"]
                            st.markdown(f'<div class="response-card">{info}</div>', unsafe_allow_html=True)
                            
                            # Add to My Medications button
                            if st.button("➕ Add to My Medications"):
                                new_med = {
                                    "name": query,
                                    "added_date": datetime.now().strftime("%Y-%m-%d"),
                                    "details": info
                                }
                                st.session_state.medications.append(new_med)
                                st.success(f"Added {query} to My Medications")
                        else:
                            st.error("Failed to fetch medication information")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            st.subheader("Quick Tools")
            st.button("🔄 Drug Interaction Checker")
            st.button("🧮 Dosage Calculator")
            st.button("🏥 Find Nearby Pharmacies")
    
    # Tab 2: My Medications
    with tabs[1]:
        st.subheader("My Medications")
        
        # Add New Medication Form
        with st.expander("➕ Add New Medication"):
            with st.form("add_medication_form"):
                med_name = st.text_input("Medication Name")
                col1, col2 = st.columns(2)
                with col1:
                    dosage = st.text_input("Dosage")
                    manufacturer = st.text_input("Manufacturer")
                with col2:
                    expiry_date = st.date_input("Expiry Date")
                    storage_info = st.text_input("Storage Instructions")
                
                usage_instructions = st.text_area("Usage Instructions")
                prescription = st.file_uploader("Upload Prescription", type=["pdf", "jpg", "png"])
                
                if st.form_submit_button("Add Medication"):
                    if med_name:
                        new_med = {
                            "name": med_name,
                            "dosage": dosage,
                            "manufacturer": manufacturer,
                            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                            "storage_info": storage_info,
                            "usage_instructions": usage_instructions,
                            "added_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.medications.append(new_med)
                        st.success(f"Added {med_name} to your medications")
        
        # Display Medications
        if st.session_state.medications:
            for med in st.session_state.medications:
                with st.expander(f"💊 {med['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Dosage:** {med.get('dosage', 'N/A')}")
                        st.write(f"**Manufacturer:** {med.get('manufacturer', 'N/A')}")
                        st.write(f"**Added Date:** {med.get('added_date', 'N/A')}")
                    with col2:
                        st.write(f"**Expiry Date:** {med.get('expiry_date', 'N/A')}")
                        st.write(f"**Storage:** {med.get('storage_info', 'N/A')}")
                    
                    st.write("**Usage Instructions:**")
                    st.write(med.get('usage_instructions', 'N/A'))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.button("📝 Edit", key=f"edit_{med['name']}")
                    with col2:
                        st.button("⏰ Set Reminder", key=f"reminder_{med['name']}")
                    with col3:
                        st.button("🗑️ Delete", key=f"delete_{med['name']}")
        else:
            st.info("No medications added yet. Use the form above to add medications.")
    
    # Tab 3: Reminders
    with tabs[2]:
        st.subheader("Medication Reminders")
        
        # Add New Reminder
        with st.expander("➕ Add New Reminder"):
            with st.form("add_reminder_form"):
                medication = st.selectbox(
                    "Select Medication",
                    [med["name"] for med in st.session_state.medications] if st.session_state.medications else ["No medications added"]
                )
                time = st.time_input("Reminder Time")
                frequency = st.selectbox(
                    "Frequency",
                    ["Daily", "Twice Daily", "Every 8 hours", "Weekly", "Monthly"]
                )
                notes = st.text_input("Additional Notes")
                
                if st.form_submit_button("Set Reminder"):
                    if medication != "No medications added":
                        new_reminder = {
                            "medication": medication,
                            "time": time.strftime("%H:%M"),
                            "frequency": frequency,
                            "notes": notes,
                            "active": True
                        }
                        st.session_state.reminders.append(new_reminder)
                        st.success(f"Reminder set for {medication}")
        
        # Display Reminders
        if st.session_state.reminders:
            for reminder in st.session_state.reminders:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"**{reminder['medication']}**")
                        st.write(f"Time: {reminder['time']}")
                    with col2:
                        st.write(f"Frequency: {reminder['frequency']}")
                        st.write(f"Notes: {reminder['notes']}")
                    with col3:
                        st.button("🔕 Disable", key=f"disable_{reminder['medication']}_{reminder['time']}")
                    st.markdown("---")
        else:
            st.info("No reminders set. Add a reminder using the form above.")
    
    # Tab 4: Symptoms Tracker
    with tabs[3]:
        st.subheader("Symptoms Tracker")
        
        # Add New Symptom Entry
        with st.expander("➕ Add New Symptom Entry"):
            with st.form("add_symptom_form"):
                col1, col2 = st.columns(2)
                with col1:
                    symptom_date = st.date_input("Date")
                    symptom_type = st.text_input("Symptom")
                with col2:
                    severity = st.slider("Severity", 1, 10, 5)
                    related_med = st.selectbox(
                        "Related Medication",
                        ["None"] + [med["name"] for med in st.session_state.medications]
                    )
                
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Add Entry"):
                    new_symptom = {
                        "date": symptom_date.strftime("%Y-%m-%d"),
                        "symptom": symptom_type,
                        "severity": severity,
                        "medication": related_med,
                        "notes": notes
                    }
                    st.session_state.symptoms.append(new_symptom)
                    st.success("Symptom entry added successfully")
        
        # Display Symptom History
        if st.session_state.symptoms:
            st.subheader("Symptom History")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_date = st.date_input("Filter by date")
            with col2:
                filter_med = st.selectbox(
                    "Filter by medication",
                    ["All"] + [med["name"] for med in st.session_state.medications]
                )
            
            # Display filtered symptoms
            for symptom in st.session_state.symptoms:
                if (filter_med == "All" or symptom["medication"] == filter_med):
                    with st.expander(f"🤒 {symptom['symptom']} - {symptom['date']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Severity:** {symptom['severity']}/10")
                            st.write(f"**Related Medication:** {symptom['medication']}")
                        with col2:
                            st.write(f"**Notes:** {symptom['notes']}")
        else:
            st.info("No symptom entries yet. Use the form above to track your symptoms.")
    
    # Tab 5: AI Assistant
    with tabs[4]:
        st.subheader("AI Medication Assistant")
        
        # Chat interface
        if 'ai_chat_history' not in st.session_state:
            st.session_state.ai_chat_history = []
        
        # Display chat history
        for message in st.session_state.ai_chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        user_question = st.chat_input("Ask about your medications...")
        
        if user_question:
            # Add user message to chat history
            st.session_state.ai_chat_history.append({"role": "user", "content": user_question})
            
            # Get AI response
            try:
                response = requests.post(f"{API_URL}/chat", json={
                    "user_id": st.session_state.user_id,
                    "user_name": "User",
                    "query": f"Medication question: {user_question}"
                })
                
                if response.status_code == 200:
                    ai_response = response.json()["answer"]
                    st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                else:
                    st.error("Failed to get response from AI")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Quick question suggestions
        st.markdown("### Quick Questions")
        quick_questions = [
            "What are common side effects?",
            "How should I store my medications?",
            "What should I do if I miss a dose?",
            "Can I take this with other medications?",
            "What are the signs of an allergic reaction?"
        ]
        
        for question in quick_questions:
            if st.button(f"🔹 {question}", key=f"quick_{question}"):
                # Simulate clicking the question into the chat
                st.session_state.ai_chat_history.append({"role": "user", "content": question})
                st.rerun()

# ... (rest of the code remains the same)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by Sriman</p>
        <p style='font-size: 0.8em'>Disclaimer: This is an AI assistant and should not replace professional medical advice.</p>
    </div>
    """,
    unsafe_allow_html=True
)