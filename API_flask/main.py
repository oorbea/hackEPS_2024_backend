from flask import Flask, jsonify, request
import pandas as pd
from ai_model import AIModel

# Inicializar Flask app
app = Flask(__name__)

# Inicializar el modelo AI
tramits_file = '../data/tramits.csv'
accions_file = '../data/accionsPreprocesadas1.csv'


# Inicializa el modelo
model = AIModel(tramits_file='tramits.csv', accions_file='accions.csv')

# Cargar el modelo guardado
model.load_model(knn_path='../modelos/knn_model.joblib', encoder_path='../modelos/label_encoder.pkl')

# Hacer predicciones




# Cargar datos de tramits para detalles
try:
    tramits_data = pd.read_csv(tramits_file)
    tramits_dict = tramits_data.set_index('Id')[['Titol', 'Vigent']].to_dict(orient='index')
except FileNotFoundError:
    raise FileNotFoundError(f"El archivo {tramits_file} no existe.")

@app.route('/predict/<string:current_session>/<string:current_tramite>', methods=['GET'])
def recommendation(current_session, current_tramite):
    """
    Genera recomendaciones basadas en el trámite actual.
    """
    try:
        # Obtener recomendaciones
        recommendations = model.predict_tramites(current_tramite= current_tramite, n_recommendations=5)

        # Filtrar el trámite actual y mapear detalles
        filtered_recommendations = [
            {
                "Id": rec,
                "Titol": tramits_dict.get(rec, {}).get('Titol', "Unknown"),
                "Vigent": tramits_dict.get(rec, {}).get('Vigent', "Unknown")
            }
            for rec in recommendations if rec != current_tramite
        ]

        return jsonify(filtered_recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar si la API está activa."""
    return jsonify({"message": "Python API is running."}), 200

# Ejecutar la app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
