from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app) 

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"reply": "Mensaje vacío recibido."}), 400

        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un terapeuta empático y profesional que analiza emocionalmente lo que el usuario te dice."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Ocurrió un error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
