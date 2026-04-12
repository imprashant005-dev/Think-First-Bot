from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Securely load the API key from the environment
my_api_key = os.environ.get("GEMINI_API_KEY")

if not my_api_key:
    raise ValueError(
        "No API key found. Please set the GEMINI_API_KEY environment variable."
    )

genai.configure(api_key=my_api_key)

system_instruction = """
You are a 'Think First' educational chatbot. 

CRITICAL BEHAVIOR RULES (STRICTLY ENFORCED):
1. INITIAL REQUEST: When a user asks a question or gives a prompt, DO NOT give the direct answer immediately. Instead, ask EXACTLY ONE short, concise hint or question related to their topic to make them think. Keep it to 1-2 sentences.
2. THE USER'S REPLY: When the user replies to your hint/question (whether their guess is right, wrong, or if they say "give me the answer" / "I don't know"), you MUST immediately provide the FULL, complete, and detailed answer to their original request.
3. NO ENDLESS LOOPS: NEVER ask a second follow-up question. Once the user replies to your first hint, the 'guessing game' is over. You must surrender the full answer.
4. Maintain a friendly, encouraging, and gamified tone.
"""

model = genai.GenerativeModel(model_name="gemma-3-27b-it")

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                f"SYSTEM INSTRUCTION (Read and follow this strictly):\n{system_instruction}"
            ],
        },
        {
            "role": "model",
            "parts": [
                "Understood! I am the Think First educational chatbot. I will ask exactly one short hint/question, and immediately reveal the full answer on the second turn or if the user asks for it. I am ready."
            ],
        },
    ]
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return jsonify({"error": "An error occurred on the server."}), 500


# Removed debug=True for production
if __name__ == "__main__":
    app.run()
