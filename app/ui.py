import streamlit as st
import requests
import os
import re
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

# Optional: enable logging
logging.basicConfig(level=logging.INFO)


def clean_bot_response(content):
    # Remove <think>...</think> and strip extra whitespace
    cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return cleaned


def query_api(user_message):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "model": "deepseek-ai/DeepSeek-R1-0528"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and data["choices"]:
            bot_message = data["choices"][0]["message"]
            if isinstance(bot_message, dict) and "content" in bot_message:
                raw_content = bot_message["content"]
                cleaned_content = clean_bot_response(raw_content)
                return cleaned_content
            else:
                return "⚠️ No valid content in the API response."
        else:
            return "⚠️ No valid response from the API."
    except Exception as e:
        logging.error(f"API request failed: {e}")
        return f"❌ Error: {str(e)}"


# Streamlit UI
st.title("Chatbot UI")
user_message = st.text_input("Enter your message:", "")

if st.button("Send"):
    if user_message.strip():
        bot_response = query_api(user_message)
        st.text_area("Bot Response", bot_response, height=200)
    else:
        st.warning("Please enter a message.")
