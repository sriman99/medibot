from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
import os

google_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-1.5-flash",
    temperature=0.7
)

health_report_prompt = PromptTemplate(
    input_variables=["user_name", "age", "gender", "medical_history", "current_medications"],
    template=(
        "Generate a health report for the following details:\n"
        "Name: {user_name}\nAge: {age}\nGender: {gender}\nMedical History: {medical_history}\nCurrent Medications: {current_medications}.\n"
        "Provide a detailed summary and potential recommendations for further care."
    )
)

def generate_health_report(user_name, age, gender, medical_history, current_medications):
    prompt = health_report_prompt.format(
        user_name=user_name, age=age, gender=gender,
        medical_history=medical_history, current_medications=current_medications
    )
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])

    if isinstance(response, AIMessage):
        return response.content.strip()
    return "Failed to generate health report. Please try again."
