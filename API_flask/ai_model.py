import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors

class AIModel:
    def __init__(self, tramits_file, accions_file, sample_fraction=0.1):
        self.tramits_file = tramits_file  # Ruta a tramits.csv
        self.accions_file = accions_file  # Ruta a accions.csv
        self.sample_fraction = sample_fraction
        self.encoder = LabelEncoder()
        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
        self.unique_tramites = None
        self.X = None

    def load_and_preprocess_data(self):
        """
        Carga y preprocesa los datos.
        """
        # Carga los datos
        tramits = pd.read_csv(self.tramits_file)
        accions = pd.read_csv(self.accions_file)
        # self.tramits = tramits
        # # Validación de columnas
        # required_accions_columns = ['Tramit', 'Sessio']
        # required_tramits_columns = ['Id']
        # if not set(required_accions_columns).issubset(accions.columns):
        #     raise ValueError("Faltan columnas requeridas en accions.csv.")
        # if not set(required_tramits_columns).issubset(tramits.columns):
        #     raise ValueError("Faltan columnas requeridas en tramits.csv.")

        # # Procesar fechas y ordenar
        # accions['Data'] = pd.to_datetime(accions['Data'], errors='coerce')
        # accions = accions.dropna(subset=['Data']).sort_values(by=['Sessio', 'Data'])

        # # Generar pares de trámites consecutivos por sesión
        # sequences = accions.groupby('Sessio')['Tramit'].apply(list).reset_index()
        # pairs = [
        #     (seq[i], seq[i + 1])
        #     for seq in sequences['Tramit'] if len(seq) > 1
        #     for i in range(len(seq) - 1)
        # ]


        # Codificar trámites
        accions_sample = accions.sample(10000)

        self.unique_tramites = accions_sample['Tramit']
        print(tramits.columns)
        # TODO En lugar de acciones, habria que fitear con un dataset preprocesado guay
        interaxion_matrix = pd.get_dummies(accions_sample["Tramit"].apply(pd.Series).stack()).groupby(level=0).sum()[self.unique_tramites].fillna(0).astype(int).transpose()
        matrix_scaled = pd.DataFrame(StandardScaler().fit_transform(interaxion_matrix),
                                     index=interaxion_matrix.index,
                                     columns=interaxion_matrix.columns)
        self.encoder.fit(matrix_scaled)

        # df_pairs = pd.DataFrame(pairs, columns=['Current_Tramite', 'Next_Tramite'])
        # df_pairs['Current_Tramite'] = self.encoder.transform(df_pairs['Current_Tramite'])
        # df_pairs['Next_Tramite'] = self.encoder.transform(df_pairs['Next_Tramite'])

        # # Muestreo
        # if self.sample_fraction < 1.0:
        #     df_pairs = df_pairs.sample(frac=self.sample_fraction, random_state=42)
        # # Preparar datos para el modelo
        # self.X = np.array(df_pairs['Current_Tramite']).reshape(-1, 1)
        # print(f"Datos preprocesados: {len(self.X)} filas listas para el modelo.")

    def train_model(self):
        """
        Entrena el modelo KNN.
        """
        if self.X is None:
            raise ValueError("No hay datos preprocesados. Ejecuta `load_and_preprocess_data` primero.")
        self.knn.fit(self.X)
        print("Modelo KNN entrenado correctamente.")

    def predict_tramites(self, current_tramite, n_recommendations=5):
        """
        Predice los próximos trámites basados en un trámite actual.
        """
        if current_tramite not in self.encoder.classes_:
            print(f"Trámite '{current_tramite}' no encontrado.")
            return []

        # Convertir el trámite actual a su índice codificado
        current_index = self.encoder.transform([current_tramite])[0]
        current_vector = np.array([[current_index]])
        predicts = {}
        # Obtener las recomendaciones directamente
        distances, indices = self.knn.kneighbors(current_vector, n_neighbors=n_recommendations)
        # print("DISTANCES")
        # print(distances.flatten())
        # print("INDICES")
        # print(indices.flatten())
        # for i in range(0, len(distances.flatten())):
        #     predicts[self.unique_tramites[indices.flatten()[i]]] = distances.flatten()[i]
        # print(predicts)
        return [self.unique_tramites[idx] for idx in indices[0] if idx < len(self.unique_tramites)]


# Configuración del modelo
