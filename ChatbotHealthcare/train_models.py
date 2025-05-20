import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Embedding, LSTM, Dense, Dropout, Flatten
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import pickle

# --------- CONFIG ---------
MAX_LEN = 20
VOCAB_SIZE = 2000
EMBED_DIM = 64

# --------- LOAD DATA ---------
# Replace these with your actual data loading logic
# For intent model (text classification)
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)
    texts = []
    labels = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            texts.append(pattern)
            labels.append(intent['tag'])

# For symptom checker (multi-label classification)
with open('relevant_symptom_names_filtered.json', 'r', encoding='utf-8') as f:
    symptom_names = json.load(f)

# Dummy data for symptom checker (replace with your real data)
# Each sample: (symptom_vector, disease_label)
symptom_data = [
    (np.random.randint(0, 2, len(symptom_names)).tolist(), 'Bệnh A') for _ in range(200)
]
symptom_vectors = [x[0] for x in symptom_data]
disease_labels = [x[1] for x in symptom_data]

# --------- TOKENIZER & ENCODERS ---------
tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN, truncating='post')

lbl_encoder = LabelEncoder()
encoded_labels = lbl_encoder.fit_transform(labels)

symptom_encoder = LabelEncoder()
encoded_diseases = symptom_encoder.fit_transform(disease_labels)

# --------- INTENT MODEL ---------
intent_model = Sequential([
    InputLayer(input_shape=(MAX_LEN,)),
    Embedding(VOCAB_SIZE, EMBED_DIM),
    LSTM(64, return_sequences=False),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(len(lbl_encoder.classes_), activation='softmax')
])
intent_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
intent_model.summary()

intent_model.fit(padded_sequences, encoded_labels, epochs=10, batch_size=16)
intent_model.save('intent_chatbot_model.keras')

# --------- SYMPTOM CHECKER MODEL ---------
symptom_model = Sequential([
    InputLayer(input_shape=(len(symptom_names),)),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(len(symptom_encoder.classes_), activation='softmax')
])
symptom_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
symptom_model.summary()

symptom_model.fit(np.array(symptom_vectors), encoded_diseases, epochs=10, batch_size=16)
symptom_model.save('symptom_checker_model_filtered.keras')

# --------- SAVE TOKENIZER & ENCODERS ---------
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('label_encoder.pickle', 'wb') as handle:
    pickle.dump(lbl_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('symptom_label_encoder_filtered_EN.pickle', 'wb') as handle:
    pickle.dump(symptom_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Training complete. Models and encoders saved.')
