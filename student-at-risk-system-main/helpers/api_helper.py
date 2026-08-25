from typing import Literal

from pydantic import BaseModel, Field


class StudentInputData(BaseModel):
    studytime: int = Field(ge=1, le=4)
    failures: int = Field(ge=0, le=3)
    schoolsup: Literal["yes", "no"]
    famsup: Literal["yes", "no"]
    activities: Literal["yes", "no"]
    higher: Literal["yes", "no"]
    internet: Literal["yes", "no"]
    famrel: int = Field(ge=1, le=5)
    health: int = Field(ge=1, le=5)
    absences: int = Field(ge=0)


def get_student_prediction_result(prediction: int, probability):
    result = "At risk" if prediction == 1 else "Not at risk"
    prob_at_risk = round(float(probability[1]), 3)
    prob_not_at_risk = round(float(probability[0]), 3)
    prob_percentage = (
        round(prob_at_risk * 100, 2)
        if result == "At risk"
        else round(prob_not_at_risk * 100, 2)
    )
    return {
        "result": result,
        "probability": {
            "at_risk": prob_at_risk,
            "not_at_risk": prob_not_at_risk,
        },
        "model_percentage": prob_percentage,
        "human_required": True,
    }
