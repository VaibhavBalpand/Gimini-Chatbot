import os
import streamlit as st
import google.generativeai as gen_ai
import random

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key="AIzaSyBuM8g8Z0EWKU8LWwbV-LO6GtLP5cE4epE")
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Function to generate contextual recommendations
def get_recommendations(user_prompt):
    # Example static recommendations (you can make these more dynamic or varied)
    all_recommendations = [
        f"What are the benefits of {user_prompt}?",
        f"How does {user_prompt} compare to other options?",
        f"What are the common issues with {user_prompt}?",
        f"Where can I find more information on {user_prompt}?",
        f"How can {user_prompt} be improved?",
        f"Are there any alternatives to {user_prompt}?",
        f"How does {user_prompt} impact industry trends?",
        f"What are user reviews saying about {user_prompt}?"
    ]

    # Randomly select 3 or 4 unique recommendations from the list
    selected_recommendations = random.sample(all_recommendations, 4)
    return selected_recommendations


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Add custom CSS to style the chat application and placeholder text
st.markdown(
    """
    <style>
    .main {
        margin-top:-10px;
        background-color: #333; /* Dark background */
        color: #f0f0f0; /* Light text color */
    }
    h1 {
        color: white !important; /* Force white color for the title */
        margin-left:100px;
    }
    hr {
        border: none;
        border-top: 2px solid white;
        margin: 10px 0;
    }
    .stMarkdown p, .stMarkdown div {
        color: white !important; /* Ensure all text in chat is white */
    }
    .st-emotion-cache-1wpj71q {
        border-radius: 20.5rem !important;
        display: flex !important;
        background-color: rgb(255, 255, 255) !important;
        width: 718px !important;
        margin-left: 11px !important;
    }
    .st-emotion-cache-90vs21 {
        position: fixed !important;
        bottom: 21px !important;
        padding-bottom: 25px !important;
        padding-top: 1rem !important;
        background-color: rgb(255, 255, 255) !important;
        z-index: 99 !important;
        height: 70px !important;
        border-radius: 61px !important;
    }
    .stTextInput input::placeholder {
        color: #333 !important; /* Darker placeholder text */
        opacity: 1; /* Ensure full opacity for the placeholder text */
    }
    .recommendations {
        margin-top: 20px;
        padding: 10px;
        background-color: #444; /* Slightly lighter background for recommendations */
        border-radius: 10px;
    }
    .recommendations h3 {
        color: #fff;
    }
    .recommendations ul {
        list-style-type: none;
        padding: 0;
    }
    .recommendations li {
        margin: 5px 0;
        color: #ddd;
        cursor: pointer; /* Indicate clickable items */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the chatbot's title and add a white horizontal line under it
st.title("🤖 Gemini Pro - ChatBot")
st.markdown("<hr>", unsafe_allow_html=True)  # Adding a white horizontal line

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message with a custom style and darker placeholder
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response with white text color
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

    # Display contextual recommendations
    recommendations = get_recommendations(user_prompt)
    st.markdown("<div class='recommendations'><h3>Recommended for you:</h3><ul>", unsafe_allow_html=True)
    for rec in recommendations:
        st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)
