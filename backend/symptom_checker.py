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

symptom_checker_prompt = PromptTemplate(
    input_variables=["symptoms"],
    template="Analyze the following symptoms: {symptoms}. Provide a possible diagnosis and recommend next steps."
)

def check_symptoms(symptoms):
    prompt = symptom_checker_prompt.format(symptoms=symptoms)
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])

    if isinstance(response, AIMessage):
        return response.content.strip()
    return "Unable to analyze symptoms at this time. Please try again."
