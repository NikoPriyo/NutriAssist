from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import joblib
from google.cloud import firestore

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Nutrition Status Prediction API with Firestore")

# Inisialisasi Firestore client
db = firestore.Client.from_service_account_json("firebase_credentials.json")

# Load model dan scaler
model = tf.keras.models.load_model("modelNN.h5")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Definisi schema request data
class NutritionInput(BaseModel):
    user_id: str  # ID unik untuk user
    umur: float
    jenis_kelamin: str  # 'laki-laki' atau 'perempuan'
    tinggi_badan: float

# Endpoint untuk prediksi dan penyimpanan ke Firestore
@app.post("/predict/")
def predict_and_store(input_data: NutritionInput):
    try:
        # Validasi input
        if input_data.jenis_kelamin.lower() not in ['laki-laki', 'perempuan']:
            raise HTTPException(status_code=400, detail="Jenis kelamin harus 'laki-laki' atau 'perempuan'")

        # Preprocessing input
        jenis_kelamin_encoded = 1 if input_data.jenis_kelamin.lower() == 'laki-laki' else 0
        user_data = np.array([[input_data.umur, input_data.tinggi_badan, jenis_kelamin_encoded]])
        user_data = scaler.transform(user_data)

        # Prediksi dengan model
        prediction = model.predict(user_data)
        predicted_class = label_encoder.inverse_transform([np.argmax(prediction)])[0]

        # Simpan hasil ke Firestore
        result_data = {
            "user_id": input_data.user_id,
            "umur": input_data.umur,
            "jenis_kelamin": input_data.jenis_kelamin,
            "tinggi_badan": input_data.tinggi_badan,
            "status_gizi": predicted_class
        }
        db.collection("predictions").document(input_data.user_id).set(result_data)

        return {"message": "Prediction stored successfully", "data": result_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk mengambil data berdasarkan user_id
@app.get("/get_prediction/{user_id}")
def get_prediction(user_id: str):
    try:
        # Ambil data dari Firestore
        doc = db.collection("predictions").document(user_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User ID not found")
        return {"message": "Prediction retrieved successfully", "data": doc.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
