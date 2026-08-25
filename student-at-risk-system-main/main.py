from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import joblib
import pandas as pd
from helpers.api_helper import StudentInputData, get_student_prediction_result


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_PATH = BASE_DIR.parent / "index.html"
MODEL_PATH = BASE_DIR / "student-at-risk-model.joblib"

model = joblib.load(MODEL_PATH)
app = FastAPI(
    title="Student At Risk System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_PATH)


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Student risk model is ready."}


@app.post("/predict")
def predict_student_at_risk(student_data: StudentInputData):
    data_frame = pd.DataFrame([student_data.model_dump()])
    prediction = model.predict(data_frame)[0]
    probability = model.predict_proba(data_frame)[0]
    return get_student_prediction_result(prediction, probability)
