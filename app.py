from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
CORS(app)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API de Análisis de Sentimientos está activa."})

@app.route("/analizar", methods=["POST"])
def analizar():
    try:
        data = request.get_json()
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"reply": "Por favor proporciona un mensaje."}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un psicólogo que analiza emociones y sentimientos."},
                {"role": "user", "content": mensaje}
            ]
        )

        texto_generado = response.choices[0].message.content.strip()

        return jsonify({"reply": texto_generado})

    except Exception as e:
        return jsonify({"reply": f"Ocurrió un error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
