from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analizar", methods=["POST"])
def analizar():
    try:
        data = request.get_json()
        mensaje = data.get("mensaje", "")

        if not mensaje:
            return jsonify({"reply": "Mensaje vacío"}), 400

        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un terapeuta virtual que analiza emociones."},
                {"role": "user", "content": mensaje}
            ]
        )

        texto_respuesta = respuesta['choices'][0]['message']['content']
        return jsonify({"reply": texto_respuesta})

    except Exception as e:
        return jsonify({"reply": f"Ocurrió un error: {str(e)}"})
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
