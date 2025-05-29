from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

app = FastAPI()


class ChatRequest(BaseModel):
    user_message: str


@app.post("/chat")
def chat(request: ChatRequest):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": request.user_message
            }
        ],
        "model": "deepseek-ai/DeepSeek-R1-0528"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, verify=False)  # Disable SSL verification
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to the API", "details": str(e)}

    try:
        data = response.json()
    except ValueError as e:
        return {"error": "Failed to parse API response", "details": str(e)}

    if "choices" in data and data["choices"]:
        return {"bot_response": data["choices"][0]["message"]}
    else:
        return {"error": "The API response does not contain valid choices."}
