from flask import Flask, jsonify, request
import pandas as pd
from ai_model import AIModel

# Inicializar Flask app
app = Flask(__name__)

# Inicializar el modelo AI
tramits_file = './data/tramits.csv'
accions_file = './data/accionsPreprocesadas1.csv'

ai_model = AIModel(tramits_file, accions_file)
ai_model.load_and_preprocess_data()
ai_model.train_model()

# Cargar datos de tramits para detalles
try:
    tramits_data = pd.read_csv(tramits_file)
    tramits_dict = tramits_data.set_index('Id')[['Titol', 'Vigent']].to_dict(orient='index')
except FileNotFoundError:
    raise FileNotFoundError(f"El archivo {tramits_file} no existe.")

@app.route('/predict/<current_session>/<current_tramite>', methods=['GET'])
def recommendation(current_session, current_tramite):
    current_tramite = current_tramite.replace("%2F", "/")
    """
    Genera recomendaciones basadas en el trámite actual.
    """
    try:
        # Obtener recomendaciones
        recommendations = ai_model.predict_tramites(current_tramite)

        # Filtrar el trámite actual y mapear detalles
        filtered_recommendations = [
            {
                "Id": rec,
                "Titol": tramits_dict.get(rec, {}).get('Titol', "Unknown"),
                "Vigent": tramits_dict.get(rec, {}).get('Vigent', "Unknown")
            }
            for rec in recommendations if rec != current_tramite
        ]

        return jsonify({filtered_recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar si la API está activa."""
    return jsonify({"message": "Python API is running."}), 200

# Ejecutar la app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
