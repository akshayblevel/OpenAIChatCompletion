import os
from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI

app = Flask(__name__)

API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://akkioai.openai.azure.com/")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "akkigpt-4")

client = AzureOpenAI(
    api_key=API_KEY,
    api_version=API_VERSION,
    azure_endpoint=AZURE_ENDPOINT
)


@app.route("/")
def index():
    """Render the chatbot UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests from the UI."""
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"reply": "Please enter a valid message."}), 400

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=150,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)