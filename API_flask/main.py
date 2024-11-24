from flask import Flask, jsonify, request
import pandas as pd
from ai_model import AIModel
import pickle
import numpy as np

# Inicializar Flask app
app = Flask(__name__)

# Inicializar el modelo AI
tramits_file = '../data/tramits.csv'
accions_file = '../data/accionsPreprocesadas1.csv'


# Inicializa el modelo


with open("onehot.pkl", 'rb') as onehotfile:
    onehot = pickle.load(onehotfile)
with open("nearest.pkl", 'rb') as file_:
    nn = pickle.load(file_)
with open("all_tramits.pkl", 'rb') as file_:
    all_tramits = pickle.load(file_)

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
    # try:
        # Obtener recomendaciones
    example_first = onehot.transform([[current_tramite]]).toarray()
    input_ = np.zeros_like(all_tramits[0])
    input_[:774 // 2] = example_first[0][:774 // 2]
    input_[774 // 2:] = 0
    output_ = nn.kneighbors(input_[np.newaxis])[1]
    _, tramits_idx = np.where(all_tramits[output_][0, :, 387:] ==1)
    possible_tramits = list(onehot.categories_[0][tramits_idx])
    possible_tramits = list(filter(lambda x: x != current_tramite, possible_tramits))
    filtered_recommendations = [
        {
            "Id": rec,
            "Titol": tramits_dict.get(rec, {}).get('Titol', "Unknown"),
            "Vigent": tramits_dict.get(rec, {}).get('Vigent', "Unknown")
        }
        for rec in possible_tramits #if rec != current_tramite
    ]

    return jsonify(filtered_recommendations)
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar si la API está activa."""
    return jsonify({"message": "Python API is running."}), 200

# Ejecutar la app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
