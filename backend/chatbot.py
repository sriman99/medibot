# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import AIMessage, HumanMessage
# from langchain.prompts import PromptTemplate
# import os

# google_api_key = os.getenv("GEMINI_API_KEY")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/srima/Downloads/stoked-clone-446116-k4-42a4dd57267c.json"

# llm = ChatGoogleGenerativeAI(
#     google_api_key=google_api_key,
#     model="gemini-1.5-flash",
#     temperature=0.7
# )

# chat_prompt = PromptTemplate(
#     input_variables=["user_name", "query"],
#     template=(
#         "Provide a thoughtful and informative response to the following query from {user_name}: {query}. "
#         "Ensure the response is supportive and helpful, while highlighting that it is not a substitute for professional healthcare."
#     )
# )

# def handle_chat_query(user_name, query):
#     prompt = chat_prompt.format(user_name=user_name, query=query)
#     message = HumanMessage(content=prompt)
#     response = llm.invoke([message])

#     if isinstance(response, AIMessage):
#         return response.content.strip()
#     return "Oops, something went wrong. Let me try again."

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
import os

# Set the Google API key and credentials for Gemini API
google_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/srima/Downloads/stoked-clone-446116-k4-42a4dd57267c.json"

# Initialize the ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-1.5-flash",
    temperature=0.7
)

# Define the prompt template
chat_prompt = PromptTemplate(
    input_variables=["user_name", "query"],
    template=(
        "Provide a thoughtful and informative response to the following query from {user_name}: {query}. "
        "Ensure the response is supportive and helpful, while highlighting that it is not a substitute for professional healthcare."
    )
)

def handle_chat_query(user_id, user_name, query):
    # Ensure that if 'user_name' is not provided, default to 'default_user'
    user_name = user_name if user_name else "user"

    # Format the prompt with the user_name and query
    prompt = chat_prompt.format(user_name=user_name, query=query)

    # Create the HumanMessage with the formatted prompt
    message = HumanMessage(content=prompt)

    try:
        # Invoke the model with the message
        response = llm.invoke([message])

        # Check if the response is of type AIMessage and return the content
        if isinstance(response, AIMessage):
            return response.content.strip()

    except Exception as e:
        # Handle any exceptions that occur during the request
        return f"Oops, something went wrong. Error: {str(e)}"

    # Return a fallback message in case of any unexpected response type
    return "Oops, something went wrong. Let me try again."