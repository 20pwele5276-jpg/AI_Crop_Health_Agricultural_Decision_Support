from app.services.crop_health_detector import predict_condition


def test_heat_stress_prediction():
    condition, confidence = predict_condition(
        temperature=42,
        humidity=40,
        soil_moisture=30,
        soil_ph=6.8,
        nitrogen=60,
        phosphorus=40,
        potassium=45,
    )

    assert condition == "Heat_Stress"
    assert confidence > 0.90


def test_prediction_returns_confidence():
    condition, confidence = predict_condition(
        temperature=25,
        humidity=70,
        soil_moisture=55,
        soil_ph=6.8,
        nitrogen=60,
        phosphorus=40,
        potassium=45,
    )

    assert isinstance(condition, str)
    assert 0 <= confidence <= 1