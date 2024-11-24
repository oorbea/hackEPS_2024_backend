from ai_model import AIModel
import pandas as pd

tramits_file = '../data/tramits.csv'
accions_file = '../data/accionsPreprocesadas1.csv'

# Inicializar y ejecutar el modelo
model = AIModel(tramits_file=tramits_file, accions_file=accions_file)

model.load_and_preprocess_data()


model.train_model()




#accions = pd.read_csv(accions_file)

# Evaluar predicciones
#total_tramites = 0
#correct_predictions = 0

# Iterar sobre todas las sesiones y sus secuencias
# for session, group in accions.groupby('Sessio'):
#     tramits_sequence = group.sort_values(by='Data')['Tramit'].tolist()
#     for i in range(len(tramits_sequence) - 1):
#         current_tramite = tramits_sequence[i]
#         next_tramite = tramits_sequence[i + 1]
        
#         # Obtener predicciones
#         recomendaciones = model.predict_tramites(current_tramite=current_tramite, n_recommendations=5)
        
#         # Verificar si el próximo trámite está en las recomendaciones
#         if next_tramite in recomendaciones:
#             correct_predictions += 1
        
#         total_tramites += 1

# # Resultados
# accuracy = correct_predictions / total_tramites if total_tramites > 0 else 0
# print(f"Total trámites evaluados: {total_tramites}")
# print(f"Predicciones correctas: {correct_predictions}")
# print(f"Precisión del modelo: {accuracy:.2%}")


