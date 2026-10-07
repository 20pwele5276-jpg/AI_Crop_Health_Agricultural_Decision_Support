import random

import pandas as pd


random.seed(42)


def generate_dataset():
    rows = []

    conditions = {
        "Healthy": 200,
        "Water_Stress": 200,
        "Nutrient_Deficiency": 200,
        "Heat_Stress": 200,
        "Disease_Risk": 200,
    }

    for condition, count in conditions.items():
        for _ in range(count):

            if condition == "Healthy":
                temperature = random.uniform(20, 30)
                humidity = random.uniform(60, 80)
                soil_moisture = random.uniform(45, 70)
                soil_ph = random.uniform(6.0, 7.5)
                nitrogen = random.uniform(50, 80)
                phosphorus = random.uniform(30, 60)
                potassium = random.uniform(30, 60)

            elif condition == "Water_Stress":
                temperature = random.uniform(25, 38)
                humidity = random.uniform(30, 60)
                soil_moisture = random.uniform(10, 35)
                soil_ph = random.uniform(5.8, 7.8)
                nitrogen = random.uniform(40, 75)
                phosphorus = random.uniform(25, 55)
                potassium = random.uniform(25, 55)

            elif condition == "Nutrient_Deficiency":
                temperature = random.uniform(20, 32)
                humidity = random.uniform(50, 80)
                soil_moisture = random.uniform(35, 65)
                soil_ph = random.uniform(5.5, 8.0)
                nitrogen = random.uniform(10, 35)
                phosphorus = random.uniform(10, 30)
                potassium = random.uniform(10, 30)

            elif condition == "Heat_Stress":
                temperature = random.uniform(35, 45)
                humidity = random.uniform(25, 55)
                soil_moisture = random.uniform(20, 50)
                soil_ph = random.uniform(5.8, 7.8)
                nitrogen = random.uniform(40, 75)
                phosphorus = random.uniform(25, 55)
                potassium = random.uniform(25, 55)

            else:
                temperature = random.uniform(24, 35)
                humidity = random.uniform(70, 95)
                soil_moisture = random.uniform(45, 80)
                soil_ph = random.uniform(5.5, 7.5)
                nitrogen = random.uniform(30, 70)
                phosphorus = random.uniform(20, 50)
                potassium = random.uniform(20, 50)

            rows.append(
                [
                    temperature,
                    humidity,
                    soil_moisture,
                    soil_ph,
                    nitrogen,
                    phosphorus,
                    potassium,
                    condition,
                ]
            )

    columns = [
        "temperature",
        "humidity",
        "soil_moisture",
        "soil_ph",
        "nitrogen",
        "phosphorus",
        "potassium",
        "condition",
    ]

    data = pd.DataFrame(rows, columns=columns)

    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    data.to_csv("data/crop_health_data.csv", index=False)

    print("Dataset created successfully.")
    print(f"Rows: {len(data)}")
    print(data["condition"].value_counts())


if __name__ == "__main__":
    generate_dataset()