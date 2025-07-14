from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# A4F API credentials
a4f_api_key = "ddc-a4f-0293b06a91da4c2abf9fe22161cf2652"
a4f_base_url = "https://api.a4f.co/v1"

# Initialize client
client = OpenAI(
    api_key=a4f_api_key,
    base_url=a4f_base_url,
)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("✅ Form data received:", data)

        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid input format"}), 400

        scores = list(data.values())
        average = sum(scores) / len(scores)

        # Compute stress level
        if average <= 2.5:
            level = "Low"
        elif average <= 3.5:
            level = "Medium"
        else:
            level = "High"

        # Format prompt
        formatted_input = "\n".join([f"{k.replace('_', ' ').title()}: {v}/5" for k, v in data.items()])
        prompt = f"""
You are a helpful mental wellness assistant.

A user has submitted the following stress ratings:
{formatted_input}

Please give 3 personalized and practical suggestions to help reduce stress and improve emotional well-being. Be specific, empathetic, and concise.
"""

        # Call A4F model
        completion = client.chat.completions.create(
            model="provider-3/gpt-4",
            messages=[
                { "role": "system", "content": "You are a helpful assistant." },
                { "role": "user", "content": prompt }
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Parse response safely
        message = completion.choices[0].message.content.strip()
        suggestions = [s.strip("-•123. ").strip() for s in message.split("\n") if s.strip()]

        return jsonify({
    "stress_level": level,
    "suggestions": suggestions,
    "scores": data  
    })


    except Exception as e:
        print("❌ Error during prediction:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
