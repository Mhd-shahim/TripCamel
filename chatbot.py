import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System message defining the assistant's role
initial_message = [
    {
        "role": "system",
        "content": (
            "You are a trip planner in Dubai. You are an expert in Dubai tourism, "
            "locations, food, events, and activities. You help users plan their vacation professionally. "
            "Your name is TripCamel, short form DG. Your responses should not exceed 200 words. "
            "Always ask questions to help users plan their trip. Finally, provide a day-wise itinerary."
        ),
    },
    {
        "role": "assistant",
        "content": "Hello! I'm TripCamel (TC). How can I assist you in planning your dream trip to Dubai? 🌟",
    },
]

# Function to fetch responses from OpenAI
def get_response_from_llm(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Sorry, I encountered an error while generating a response. Please try again."

# Initialize chat history if not already set
if "messages" not in st.session_state:
    st.session_state.messages = initial_message

# Streamlit UI
st.set_page_config(page_title="TripCamel - Your Trip Planner", page_icon="🕌")
st.title("🐫 TripCamel - AI Trip Planner")


# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_message = st.chat_input("Ask me anything about your Dubai trip...")

if user_message:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Limit chat history for performance
    max_history = 10
    recent_messages = st.session_state.messages[-max_history:]

    # Get response with loading indicator
    with st.spinner("TripCamel is planning your trip..."):
        response = get_response_from_llm(recent_messages)

    # Add response to chat history
    response_message = {"role": "assistant", "content": response}
    st.session_state.messages.append(response_message)

    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)
