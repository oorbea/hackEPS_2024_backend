from ai_model_deep import DeepLearningAIModel

tramits_file = '../data/tramits.csv'
accions_file = '../data/accionsPreprocesadas1.csv'

model = DeepLearningAIModel(tramits_file=tramits_file, accions_file= accions_file, max_sequence_length=10)
model.load_and_preprocess_data()
model.build_model()
model.train_model(epochs=1, batch_size=1)
model.save_model("my_model.h5", "encoder.pkl")
