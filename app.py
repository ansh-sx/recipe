import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure your Gemini API key
GEMINI_API_KEY = "AIzaSyACwT0YIrsPB6JqhUaVPG3I4IhZljchhyw"
genai.configure(api_key=GEMINI_API_KEY)

# Set the generation configuration
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a smart recipe maker who makes creative recipes based on the ingredients. "
                       "Please type your answer in steps including an emoji also after the emoji related to that step. "
                       "Only one emoji and write emoji first then the content line. "
                       "Also write the name of the recipe in a different attribute.",
)

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    try:
        # Get user input from the request JSON
        data = request.get_json()
        user_input = data.get('input', '')

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Start a chat session and send the user's input
        chat_session = model.start_chat()
        response = chat_session.send_message(user_input)

        # Check the response and return the generated recipe
        recipe_name = response.text.get("recipe_name", "Unknown Recipe") if hasattr(response.text, "get") else "Unknown Recipe"
        steps = response.text  # Adjust this based on the actual response structure

        return jsonify({
            "recipe_name": recipe_name,
            "steps": steps
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
