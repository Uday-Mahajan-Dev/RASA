from flask import Flask, request, jsonify
from rasa.core.agent import Agent
import asyncio

app = Flask(__name__)

# Load the trained Rasa model
MODEL_PATH = "models/your_rasa_model.tar.gz"
agent = None

@app.before_first_request
def load_model():
    global agent
    agent = asyncio.run(Agent.load(MODEL_PATH))
    print("Rasa model loaded successfully!")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    responses = asyncio.run(agent.handle_text(user_message))
    # Send back just text, not JSON format
    reply_texts = [r.get("text") for r in responses if "text" in r]
    return jsonify({"reply": " ".join(reply_texts)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
