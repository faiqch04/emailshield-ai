# EmailShield AI — Deep Learning Phishing Email Detector

EmailShield AI is an academic deep learning project that classifies email text as **Safe Email** or **Phishing Email** using a trained Bidirectional Long Short-Term Memory (BiLSTM) neural network.

## Live Project

- **Prediction API:** https://emailshield-ai.vercel.app/
- **API health check:** https://emailshield-ai.vercel.app/health
- **Interactive web interface:** https://huggingface.co/spaces/faiqchaudhary/email-phishing-detector
- **Source code and model:** https://github.com/faiqch04/emailshield-ai

The API performs inference using the trained model. The frontend sends email text to the API and displays the returned prediction.

## Features

- Classifies email text as safe or phishing.
- Uses a trained BiLSTM deep learning model.
- Returns a model-reported phishing probability.
- Includes the tokenizer, trained model, and model metadata.
- Provides a REST API for predictions.
- Uses publicly available training data and free development tools.

## Dataset

**Dataset name:** Phishing Email Dataset

**Source:** [Phishing Email Dataset on Hugging Face](https://huggingface.co/datasets/zefang-liu/phishing-email-dataset)

**Direct CSV download:** [Phishing_Email.csv](https://huggingface.co/datasets/zefang-liu/phishing-email-dataset/resolve/main/Phishing_Email.csv)

The original dataset contains approximately 18,650 records. After cleaning and removing duplicate records, the project dataset contained 17,522 records:

| Class | Label | Records |
|---|---:|---:|
| Safe Email | 0 | 10,978 |
| Phishing Email | 1 | 6,544 |
| **Total** | | **17,522** |

The data was split using stratified sampling with a fixed random seed:

- Training: 14,017 records
- Validation: 1,752 records
- Testing: 1,753 records

The full CSV is downloaded from the linked source rather than stored in this repository.

## Data Preprocessing

1. Loaded the email dataset.
2. Removed duplicate records and prepared the text and labels.
3. Converted email text into integer sequences using a Keras tokenizer.
4. Limited the vocabulary to 20,000 words.
5. Used an out-of-vocabulary token for unseen words.
6. Padded and truncated sequences to 250 tokens.
7. Applied post-padding, post-truncation, and stratified train/validation/test splitting.

## Model Architecture

The classifier uses a Bidirectional LSTM neural network.

| Layer | Configuration |
|---|---|
| Embedding | 20,000 vocabulary entries, 64 dimensions |
| SpatialDropout1D | 0.2 |
| Bidirectional LSTM | 32 units |
| Dropout | 0.3 |
| Dense | 32 units, ReLU |
| Dropout | 0.2 |
| Output | 1 unit, sigmoid |

The model was trained with binary classification labels. Early stopping was used, and the best validation checkpoint was selected.

## Model Evaluation

The saved model achieved the following results on the held-out test set:

| Metric | Result |
|---|---:|
| Test accuracy | 98.23% |
| Test loss | 0.0698 |
| Macro F1-score | 98.12% |
| Weighted F1-score | 98.23% |

### Confusion Matrix

| Actual class | Predicted safe | Predicted phishing |
|---|---:|---:|
| Safe Email | 1,078 | 20 |
| Phishing Email | 11 | 644 |

These results describe performance on the project's test split. They do not guarantee the same performance on every real-world email.

## Repository Structure

```text
emailshield-ai/
├── app.py
├── requirements.txt
├── metadata.json
├── tokenizer.json
├── .python-version
├── .gitignore
├── README.md
└── model/
    ├── saved_model.pb
    ├── fingerprint.pb
    └── variables/
        ├── variables.data-00000-of-00001
        └── variables.index
```

The `model/` directory contains the TensorFlow SavedModel files. `tokenizer.json` contains the text tokenizer configuration and vocabulary. `metadata.json` records model settings and labels.

## Run Locally

Python 3.12 is recommended for the deployment environment.

1. Clone the repository:

   ```bash
   git clone https://github.com/faiqch04/emailshield-ai.git
   cd emailshield-ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the API using the application's configured entry point:

   ```bash
   python app.py
   ```

Check `app.py` for the local host and port configuration before sending requests.

## API Usage

Send a POST request to `/predict` with JSON containing an `email` field.

Example request:

```bash
curl -X POST https://emailshield-ai.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"Your email text goes here.\"}"
```

Example response structure:

```json
{
  "model": "Bidirectional LSTM",
  "prediction": "Phishing Email",
  "phishing_probability": 88.83,
  "note": "AI prediction only; verify suspicious messages independently."
}
```

The example illustrates the response format; actual results depend on the submitted text.

## Technologies

- Python
- TensorFlow / Keras
- NumPy
- Flask
- Flask-CORS
- Vercel
- Hugging Face Spaces
- Git and GitHub

## Limitations and Responsible Use

- The model classifies text; it does not independently verify sender identity, email headers, URLs, or attachments.
- The reported phishing probability is a model output and is not necessarily a calibrated real-world probability.
- A safe prediction does not prove that an email is trustworthy.
- Do not submit confidential or sensitive emails to a public demonstration.
- Always verify suspicious messages independently.

## Academic Project

EmailShield AI demonstrates the use of deep learning and natural language processing for phishing email classification. It is intended for educational and demonstration purposes, not as a replacement for professional email security systems.

## License and Dataset Attribution

The dataset is provided by its original publisher. Consult the dataset page for its current licensing and usage terms before redistributing the dataset. No separate software license is asserted by this README.
