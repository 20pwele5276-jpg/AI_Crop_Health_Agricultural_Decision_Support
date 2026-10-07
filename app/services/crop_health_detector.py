import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


DATA_PATH = "data/crop_health_data.csv"
MODEL_PATH = "models/crop_health_model.pkl"


def train_model():
    data = pd.read_csv(DATA_PATH)

    features = [
        "temperature",
        "humidity",
        "soil_moisture",
        "soil_ph",
        "nitrogen",
        "phosphorus",
        "potassium",
    ]

    X = data[features]

    encoder = LabelEncoder()
    y = encoder.fit_transform(data["condition"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(
        {
            "model": model,
            "encoder": encoder,
            "features": features,
        },
        MODEL_PATH,
    )

    return accuracy


def predict_condition(
    temperature,
    humidity,
    soil_moisture,
    soil_ph,
    nitrogen,
    phosphorus,
    potassium,
):
    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    encoder = saved_data["encoder"]
    features = saved_data["features"]

    input_data = pd.DataFrame(
        [[
            temperature,
            humidity,
            soil_moisture,
            soil_ph,
            nitrogen,
            phosphorus,
            potassium,
        ]],
        columns=features,
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities)

    condition = encoder.inverse_transform([prediction])[0]

    return condition, confidence