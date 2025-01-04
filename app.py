from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please set it in the environment variables.")

openai.api_key = OPENAI_API_KEY

# Root endpoint
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the AI Consultation API!",
        "status": "Server is running."
    })

# GPT API endpoint
@app.route("/api/gpt", methods=["POST"])
def gpt_endpoint():
    try:
        # Parse JSON request
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Invalid request. 'prompt' is required."}), 400
        
        prompt = data["prompt"]

        # Call OpenAI GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract and return response
        gpt_response = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": gpt_response})
    
    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
