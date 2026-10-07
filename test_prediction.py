from app.services.crop_health_detector import predict_condition


condition, confidence = predict_condition(
    temperature=42,
    humidity=40,
    soil_moisture=30,
    soil_ph=6.8,
    nitrogen=60,
    phosphorus=40,
    potassium=45,
)

print(f"Predicted condition: {condition}")
print(f"Confidence: {confidence:.2%}")