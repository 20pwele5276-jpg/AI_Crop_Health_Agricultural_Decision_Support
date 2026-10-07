# 🌱 AI Crop Health & Agricultural Decision Support System

An AI-powered agricultural decision support system that analyzes crop, soil, and environmental measurements to identify possible crop health conditions.

The system combines a **Machine Learning model** with an **LLM-based explanation system** and **voice input** to provide understandable and practical field insights.

## 🚀 Features

* 🌱 Crop health condition classification
* 🤖 Random Forest machine learning model
* 📊 Analysis of temperature, humidity, soil moisture, and soil pH
* 🧪 Analysis of nitrogen, phosphorus, and potassium levels
* 🎙️ Voice input for farmer field observations
* 📝 Automatic voice transcription using Whisper
* 💡 LLM-generated explanation of the detected condition
* 📈 Prediction confidence score
* 🖥️ Interactive Streamlit dashboard
* 🧪 Automated tests using pytest
* 🔐 Environment variable support for API keys

## 🧠 Conditions Detected

The machine learning model can identify five possible conditions:

* Healthy
* Water Stress
* Nutrient Deficiency
* Heat Stress
* Disease Risk

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Random Forest
* Streamlit
* Groq API
* Whisper
* LLM
* Joblib
* Python-dotenv
* Pytest
* Git & GitHub

## 📊 Dataset

The project uses a generated dataset containing **1,000 records**.

Each record contains:

* Temperature
* Humidity
* Soil Moisture
* Soil pH
* Nitrogen
* Phosphorus
* Potassium
* Crop Health Condition

The dataset contains 200 samples for each condition.

## 📈 Model Performance

The Random Forest model achieved approximately **97.5% test accuracy** on the generated dataset.

A sample heat-stress input produced:

* **Predicted Condition:** Heat Stress
* **Model Confidence:** 97%

## 🎙️ Voice Input

The application allows users to record a field observation using their microphone.

The recorded observation is transcribed using:

**Whisper Large V3 Turbo**

The transcription is then provided to the LLM along with the crop and soil measurements.

## 🤖 AI Explanation

After the machine learning model predicts a possible condition, the LLM explains:

1. What the condition may mean
2. Why the measurements may indicate it
3. What the farmer should check or consider

The system does not treat the prediction as a confirmed diagnosis.

## 📁 Project Structure

```text
AI_Crop_Health_Agricultural_Decision_Support/
│
├── app/
│   ├── __init__.py
│   ├── ui.py
│   └── services/
│       ├── __init__.py
│       ├── crop_health_detector.py
│       └── llm_service.py
│
├── data/
│   └── crop_health_data.csv
│
├── models/
│   └── crop_health_model.pkl
│
├── tests/
│   └── test_crop_health_detector.py
│
├── generate_dataset.py
├── main.py
├── test_prediction.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/20pwele5276-jpg/AI_Crop_Health_Agricultural_Decision_Support.git
```

Move into the project directory:

```bash
cd AI_Crop_Health_Agricultural_Decision_Support
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not upload the `.env` file to GitHub.

## ▶️ Running the Project

First train the machine learning model:

```bash
python main.py
```

Then start the Streamlit application:

```bash
streamlit run app/ui.py
```

Open the local Streamlit URL shown in the terminal.

## 🧪 Running Tests

Run:

```bash
pytest
```

## 🔮 Future Improvements

Possible future improvements include:

* Real agricultural datasets
* Crop-specific models
* Image-based crop disease detection
* Weather data integration
* Soil sensor integration
* Historical crop health tracking
* Multilingual farmer support
* Mobile application

## ⚠️ Disclaimer

This project is an educational AI-based decision support system.

Predictions should not be treated as confirmed agricultural diagnoses or professional agricultural advice. Field observations and qualified agricultural guidance should be used before making important decisions.

## 👩‍💻 Author

**Wajiha Gul**

BS Artificial Intelligence Student

GitHub:
https://github.com/20pwele5276-jpg


