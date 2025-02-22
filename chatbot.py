from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

chatbot = Flask(__name__)
CORS(chatbot)  

DIALOGFLOW_PROJECT_ID = "cybersecuritybot-iceg"
DIALOGFLOW_SESSION_ID = "123456"
DIALOGFLOW_URL = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{DIALOGFLOW_SESSION_ID}:detectIntent"

# Load credentials from service account JSON file
json_file_path = "cybersecuritybot-iceg-3bd171c395c5.json"  # Ensure this file exists in your project folder
credentials = service_account.Credentials.from_service_account_file(json_file_path)
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

def get_access_token():
    scoped_credentials.refresh(Request())  
    return scoped_credentials.token

@chatbot.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Message cannot be empty."}), 400

    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {"queryInput": {"text": {"text": user_message, "languageCode": "en"}}}
    
    response = requests.post(DIALOGFLOW_URL, json=data, headers=headers)
    reply = response.json().get("queryResult", {}).get("fulfillmentText", "Sorry, I didn't understand that.")

    return jsonify({"response": reply})

if __name__ == "__main__":
    chatbot.run(host="0.0.0.0", port=5000, debug=True)
