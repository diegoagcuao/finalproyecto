from flask import Blueprint, jsonify, request
from app.utils import extraer_informacion_enlace
import pickle

api_blueprint = Blueprint('api', __name__)

# Cargar el modelo y el vectorizador
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@api_blueprint.route('/clasificar_enlace', methods=['POST'])
def clasificar_enlace():
    data = request.get_json()
    enlace = data.get('enlace')

    if not enlace:
        return jsonify({"error": "Enlace no proporcionado"}), 400

    # Extraer información del enlace
    titulo, descripcion, _ = extraer_informacion_enlace(enlace)
    text = titulo + ' ' + descripcion

    # Vectorizar el texto y predecir la categoría
    X = vectorizer.transform([text])
    categoria = model.predict(X)[0]

    return jsonify({"categoria": categoria})