import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import joblib  # Para guardar y cargar el modelo KNN
import pickle  # Para guardar y cargar el LabelEncoder

class AIModel:
    def __init__(self, tramits_file, accions_file, sample_fraction=0.1, batch_size=500000):
        self.tramits_file = tramits_file  # Ruta tramits
        self.accions_file = accions_file  # Ruta acciones
        self.sample_fraction = sample_fraction
        self.batch_size = batch_size
        self.encoder = LabelEncoder()
        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.unique_tramites = None
        self.X = None

    def load_and_preprocess_data(self):
        try:
            tramits = pd.read_csv(self.tramits_file)
            accions = pd.read_csv(self.accions_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")

        # Ensure proper column names
        required_accions_columns = ['Data', 'Tramit', 'Sessio']
        required_tramits_columns = ['Id']

        if not set(required_accions_columns).issubset(accions.columns) or not set(required_tramits_columns).issubset(tramits.columns):
            raise ValueError("Missing required columns in the input files.")

        # PREPARAMOS TODO PARA UTILIZARLO Y VERIFICAMOS

        accions['Data'] = pd.to_datetime(accions['Data'], errors='coerce')
        accions = accions.dropna(subset=['Data']).sort_values(by=['Sessio', 'Data'])

        # Generate sequences and training data
        sequences = accions.groupby('Sessio')['Tramit'].apply(list).reset_index()
        pairs = [(seq[i], seq[i + 1]) for seq in sequences['Tramit'] if len(seq) > 1 for i in range(len(seq) - 1)]

        # Encode trámites
        unique_tramites = tramits['Id']
        self.encoder.fit(unique_tramites)

        df_pairs = pd.DataFrame(pairs, columns=['Current_Tramite', 'Next_Tramite'])
        df_pairs['Current_Tramite'] = self.encoder.transform(df_pairs['Current_Tramite'])
        df_pairs['Next_Tramite'] = self.encoder.transform(df_pairs['Next_Tramite'])

        # Sampling
        if self.sample_fraction < 1.0:
            df_pairs = df_pairs.sample(frac=self.sample_fraction, random_state=42)

        self.X = np.array(df_pairs['Current_Tramite']).reshape(-1, 1)
        self.unique_tramites = unique_tramites

    def train_model(self):
        self.knn.fit(self.X)
        print("KNN Model trained successfully.")

    def predict_tramites(self, current_tramite, n_recommendations=5):
        if current_tramite not in self.encoder.classes_:
            return []
        current_index = self.encoder.transform([current_tramite])[0]
        current_vector = np.array([[current_index]])
        distances, indices = self.knn.kneighbors(current_vector, n_neighbors=n_recommendations)
        return [self.unique_tramites[idx] for idx in indices[0] if idx < len(self.unique_tramites)]

    def save_model(self, knn_path, encoder_path):
        """
        Guarda el modelo KNN y el LabelEncoder en los archivos especificados.
        """
        if self.X is None:
            raise ValueError("Data not preprocessed. Call `load_and_preprocess_data()` first.")
        
        # Guardar el modelo KNN
        joblib.dump(self.knn, knn_path)
        print(f"KNN model saved to {knn_path}")

        # Guardar el encoder
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.encoder, f)
        print(f"LabelEncoder saved to {encoder_path}")

    def load_model(self, knn_path, encoder_path):
        """
        Carga el modelo KNN y el LabelEncoder desde los archivos especificados.
        """
        # Cargar el modelo KNN
        self.knn = joblib.load(knn_path)
        print(f"KNN model loaded from {knn_path}")

        # Cargar el encoder
        with open(encoder_path, 'rb') as f:
            self.encoder = pickle.load(f)
        print(f"LabelEncoder loaded from {encoder_path}")



tramits_file = '../data/tramits.csv'
accions_file = '../data/accionsPreprocesadas1.csv'
# Inicializa el modelo
model = AIModel(tramits_file=tramits_file, accions_file=accions_file)

# Cargar y preprocesar los datos
model.load_and_preprocess_data()

# Entrenar el modelo
model.train_model()

# Guardar el modelo y el codificador
model.save_model(knn_path='../modelos/knn_model.joblib', encoder_path='../modelos/label_encoder.pkl')
