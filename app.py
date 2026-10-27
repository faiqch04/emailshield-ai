
import json
import os

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "tokenizer.json"), encoding="utf-8") as f:
    tokenizer_data = json.load(f)

with open(os.path.join(BASE_DIR, "metadata.json"), encoding="utf-8") as f:
    metadata = json.load(f)

word_index = tokenizer_data["word_index"]
max_words = int(tokenizer_data["num_words"])
max_len = int(tokenizer_data["max_len"])
oov_token = tokenizer_data["oov_token"]
filters = tokenizer_data["filters"]
split_char = tokenizer_data["split"]
lowercase = tokenizer_data["lower"]

model = tf.saved_model.load(os.path.join(BASE_DIR, "model"))
predict_fn = model.signatures["serve"]

app = Flask(__name__)
CORS(app)


def prepare_email(text):
    if lowercase:
        text = text.lower()

    table = str.maketrans({char: split_char for char in filters})
    words = text.translate(table).split(split_char)

    sequence = []
    for word in words:
        if not word:
            continue

        index = word_index.get(word)
        if index is None or index >= max_words:
            index = word_index.get(oov_token, 1)

        sequence.append(index)

    sequence = sequence[:max_len]
    sequence.extend([0] * (max_len - len(sequence)))

    return np.array([sequence], dtype=np.int32)


@app.get("/")
def home():
    return jsonify({
        "project": "EmailShield AI",
        "status": "running",
        "model": "Bidirectional LSTM"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    email_text = data.get("email", "")

    if not isinstance(email_text, str) or not email_text.strip():
        return jsonify({"error": "Please provide an email to analyze."}), 400

    if len(email_text) > 20000:
        return jsonify({"error": "Email text must be 20,000 characters or fewer."}), 400

    input_tensor = tf.constant(prepare_email(email_text))
    result = predict_fn(input_layer=input_tensor)
    probability = float(next(iter(result.values())).numpy().reshape(-1)[0])

    threshold = float(metadata.get("threshold", 0.5))
    prediction = (
        "Phishing Email" if probability >= threshold else "Safe Email"
    )

    return jsonify({
        "prediction": prediction,
        "phishing_probability": round(probability * 100, 2),
        "model": metadata.get("architecture", "Bidirectional LSTM"),
        "note": "AI prediction only; verify suspicious messages independently."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
