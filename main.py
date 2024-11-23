import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Load the data
tramits = pd.read_csv('tramits.csv')  # Data for trámites
accions = pd.read_csv('accions2.csv')  # User action history

# Sort actions by session and timestamp
accions = accions.sort_values(by=['Sessio', 'Data'])

# Group by session and extract sequences of trámites
sequences = accions.groupby('Sessio')['Tramit'].apply(list).reset_index()
sequences.columns = ['Sessio', 'Sequence']

print("holiwis")
# Generate training pairs
pairs = []

for sequence in sequences['Sequence']:
    for i in range(len(sequence) - 1):
        pairs.append((sequence[i], sequence[i + 1]))

# Convert pairs to a DataFrame
df_pairs = pd.DataFrame(pairs, columns=['Current_Tramite', 'Next_Tramite'])

# One-Hot Encoding for unique trámites
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
unique_tramites = list(tramits['Id'].unique())
encoded_tramites = encoder.fit_transform(np.array(unique_tramites).reshape(-1, 1))

# Mapping dictionary (ID → Vector)
id_to_vector = dict(zip(unique_tramites, encoded_tramites))

# Convert pairs to vectors
X = np.array([id_to_vector[current] for current in df_pairs['Current_Tramite']])
y = np.array([id_to_vector[next] for next in df_pairs['Next_Tramite']])

# KNN Model
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(X)

print("KNN Model trained successfully.")

def predict_tramites(current_tramite, n_recommendations=5):
    """
    Predict the next trámites given a current trámite using the trained KNN model.
    """
    # Convert current trámite to its vector representation
    current_vector = id_to_vector[current_tramite].reshape(1, -1)
    
    # Find nearest neighbors
    distances, indices = knn.kneighbors(current_vector, n_neighbors=n_recommendations)
    
    # Decode indices to trámites IDs
    recommended_tramites = [unique_tramites[idx] for idx in indices[0]]
    return recommended_tramites

# Example prediction
current_tramite = unique_tramites[0]  # First trámite in the list
recommendations = predict_tramites(current_tramite)
print("Recommendations for trámite:", current_tramite)
print("Recommended trámites:", recommendations)
