import os
from google.cloud import dialogflow
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def detect_intent(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

@app.route("/", methods=["GET"])
def home():
    return 'Hello World'

@app.route('/chatbot', methods=['POST'])
def run_chat_bot():
    session_id = str(uuid.uuid4())
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./zibot-credentials.json"
    project_id = 'zibot-iulk'
    language_code = "en"
    data = request.get_json()
    text = data['text']
    print(text)
    response = detect_intent(project_id, session_id, text, language_code)
    print(response)
    return jsonify({"Zibot": response})

if __name__ == "__main__":
    app.run()
    debug = True 
