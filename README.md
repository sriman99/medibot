# MediBot - Your Personal Health Assistant

MediBot is an AI-powered personal health assistant that provides various health-related services such as answering health queries, symptom checking, resource finding, and generating health reports. It is built using **Streamlit** for the frontend and integrates with backend APIs built with **Flask**. MediBot aims to assist users with their health concerns and provide them with relevant resources and insights.

## Features

- **Chatbot Interaction**: Ask health-related questions and receive answers from the chatbot powered by AI.
- **Symptom Checker**: Enter symptoms to check for possible health conditions.
- **Resource Finder**: Search for health resources such as hospitals, clinics, and medical information.
- **Health Report Generator**: Generate personalized health reports based on user input, including medical history and current medications.
- **Activity Log**: View previous interactions with the assistant for reference.

## Tech Stack

- **Frontend**: Streamlit (Python library for building interactive web applications)
- **Backend**: Flask (Python web framework for API services)
- **Database**: Not included (You can integrate a database like SQLite or MongoDB for storing activity logs or reports)
- **External APIs**: Custom-built APIs for chatbot, symptom checker, and health report generation
- **Styling**: Tailwind CSS (for styling the frontend)

## Installation

### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Streamlit
- Flask
- Requests

### Steps to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/sriman99/medibot.git
    cd medi-bot
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file and adding your configuration (e.g., API keys, URLs).

4. Run the backend server:

    ```bash
    cd backend
    python app.py
    ```

5. Run the Streamlit frontend:

    ```bash
    cd frontend
    streamlit run main.py
    ```

## Usage

1. **Ask Health Questions**: Enter a health-related question and get a response from the AI-powered chatbot.
2. **Symptom Checker**: Input your symptoms to get a list of possible health conditions.
3. **Find Health Resources**: Search for health resources like hospitals, clinics, and other medical services.
4. **Generate Health Report**: Fill out a form with your health information (name, age, gender, medical history, medications) and receive a personalized health report.

## Contribution

Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.
