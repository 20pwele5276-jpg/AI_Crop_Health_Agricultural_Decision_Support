import io

import streamlit as st
from groq import Groq

from services.crop_health_detector import predict_condition
from services.llm_service import explain_condition


st.set_page_config(
    page_title="Crop Health Assistant",
    page_icon="🌱",
    layout="wide",
)


st.title("🌱 Crop Health Assistant")
st.caption(
    "AI-based agricultural decision support using crop, soil, "
    "and environmental measurements."
)

st.divider()


st.subheader("📋 Enter Field Measurements")

env_col1, env_col2, env_col3, env_col4 = st.columns(4)

with env_col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-20.0,
        max_value=60.0,
        value=25.0,
        step=1.0,
    )

with env_col2:
    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0,
    )

with env_col3:
    soil_moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=55.0,
        step=1.0,
    )

with env_col4:
    soil_ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.8,
        step=0.1,
    )


st.divider()

st.subheader("🧪 Soil Nutrient Readings")

nutrient_col1, nutrient_col2, nutrient_col3 = st.columns(3)

with nutrient_col1:
    nitrogen = st.number_input(
        "Nitrogen",
        min_value=0.0,
        max_value=150.0,
        value=60.0,
        step=1.0,
    )

with nutrient_col2:
    phosphorus = st.number_input(
        "Phosphorus",
        min_value=0.0,
        max_value=150.0,
        value=40.0,
        step=1.0,
    )

with nutrient_col3:
    potassium = st.number_input(
        "Potassium",
        min_value=0.0,
        max_value=150.0,
        value=45.0,
        step=1.0,
    )


st.divider()

st.subheader("🎙️ Field Observation")

st.write(
    "You can describe what you observe in the crop or field "
    "using your voice."
)

audio = st.audio_input("Record your field observation")

voice_observation = ""

if audio is not None:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            import os
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.warning(
                "Voice transcription is unavailable because "
                "the Groq API key is not configured."
            )
        else:
            client = Groq(api_key=api_key)

            with st.spinner("Transcribing your observation..."):
                transcription = client.audio.transcriptions.create(
                    file=(
                        "field_observation.wav",
                        io.BytesIO(audio.getvalue()),
                    ),
                    model="whisper-large-v3-turbo",
                )

            voice_observation = transcription.text

            st.success("Voice observation transcribed.")
            st.write(voice_observation)

    except Exception as error:
        st.error(f"Voice transcription error: {error}")


st.write("")

analyze = st.button(
    "🌾 Analyze Crop Health",
    use_container_width=True,
)


if analyze:

    try:
        condition, confidence = predict_condition(
            temperature,
            humidity,
            soil_moisture,
            soil_ph,
            nitrogen,
            phosphorus,
            potassium,
        )

        st.divider()

        st.subheader("🌾 Crop Health Assessment")

        result_col1, result_col2 = st.columns([2, 1])

        with result_col1:
            st.success(
                f"Possible Condition: {condition}"
            )

        with result_col2:
            st.metric(
                "Model Confidence",
                f"{confidence:.2%}",
            )

        if voice_observation:
            st.subheader("🎙️ Field Observation")
            st.write(voice_observation)

        st.divider()

        st.subheader("🤖 AI Field Explanation")

        with st.spinner("Analyzing the field readings..."):
            explanation = explain_condition(
                condition,
                temperature,
                humidity,
                soil_moisture,
                soil_ph,
                nitrogen,
                phosphorus,
                potassium,
                voice_observation,
            )

        st.write(explanation)

        st.divider()

        st.info(
            "This system provides agricultural decision support only. "
            "The result should be verified using field observations "
            "and professional agricultural advice."
        )

    except Exception as error:
        st.error(f"Error: {error}")