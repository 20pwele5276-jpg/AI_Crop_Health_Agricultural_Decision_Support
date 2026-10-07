import io
import os
from html import escape

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from services.crop_health_detector import predict_condition
from services.llm_service import explain_condition


load_dotenv()


st.set_page_config(
    page_title="Crop Health Assistant",
    page_icon="🌱",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Agriculture theme (CSS) - greens, wheat gold, soil brown, sky blue. No black.
# ---------------------------------------------------------------------------
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Nunito:wght@400;500;600;700&display=swap');

:root {
    --cream: #fbf8ec;
    --mint: #eaf4df;
    --leaf: #3e9b4f;
    --leaf-light: #7bc65a;
    --forest: #1b4332;
    --moss: #5e7f63;
    --wheat: #e8b931;
    --wheat-soft: #fbefc4;
    --soil: #8a5a33;
    --soil-soft: #f1e3d3;
    --sky: #6ec1e4;
    --card: rgba(255, 255, 255, 0.82);
    --line: rgba(62, 155, 79, 0.28);
    --shadow: 0 8px 26px rgba(62, 155, 79, 0.16);
}

/* ---------- Background ---------- */
.stApp {
    background:
        radial-gradient(700px 380px at 90% -5%, rgba(232, 185, 49, 0.28), transparent 60%),
        radial-gradient(800px 420px at 0% 0%, rgba(110, 193, 228, 0.22), transparent 60%),
        linear-gradient(180deg, #f6fbe9 0%, var(--cream) 55%, #f3ecd6 100%);
    color: var(--forest);
    font-family: 'Nunito', sans-serif;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

.block-container {
    max-width: 1120px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2rem 4.6rem;
    margin-bottom: 1.6rem;
    border-radius: 26px;
    border: 1px solid var(--line);
    background: linear-gradient(180deg, #d9f0f8 0%, #eaf6dc 62%, #dff0c8 100%);
    box-shadow: var(--shadow);
}
.sun {
    position: absolute;
    top: -34px; right: 8%;
    width: 150px; height: 150px;
    border-radius: 50%;
    background: radial-gradient(circle, #ffe27a 0%, var(--wheat) 55%, rgba(232, 185, 49, 0) 72%);
    animation: glow 4s ease-in-out infinite;
}
@keyframes glow {
    0%, 100% { transform: scale(1);    opacity: 0.9; }
    50%      { transform: scale(1.08); opacity: 1; }
}
.hills { position: absolute; left: 0; right: 0; bottom: 0; width: 100%; height: 90px; }
.hero-row { position: relative; z-index: 1; display: flex; align-items: center; gap: 1.1rem; }
.sprout {
    flex: 0 0 auto;
    width: 66px; height: 66px;
    display: grid; place-items: center;
    font-size: 2.1rem;
    border-radius: 20px;
    background: linear-gradient(145deg, #ffffff, var(--mint));
    border: 2px solid var(--leaf-light);
    box-shadow: 0 6px 16px rgba(62, 155, 79, 0.28);
    animation: sway 3.4s ease-in-out infinite;
}
@keyframes sway {
    0%, 100% { transform: rotate(-4deg); }
    50%      { transform: rotate(4deg); }
}
.hero h1 {
    margin: 0;
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: clamp(1.8rem, 4.2vw, 2.8rem);
    line-height: 1.1;
    color: var(--forest);
}
.hero p {
    margin: 0.45rem 0 0;
    color: #2f6247;
    max-width: 58ch;
    font-size: 1.02rem;
}
.chips { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
.chip {
    padding: 0.3rem 0.8rem;
    border-radius: 99px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--forest);
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid var(--line);
}
.chip.gold { background: var(--wheat-soft); border-color: rgba(232, 185, 49, 0.6); }
.chip.soil { background: var(--soil-soft); border-color: rgba(138, 90, 51, 0.35); }

/* ---------- Section titles ---------- */
.section-title {
    display: flex; align-items: center; gap: 0.5rem;
    font-family: 'Fraunces', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--forest);
    margin: 0.2rem 0 0.15rem;
}
.section-sub { color: var(--moss); font-size: 0.92rem; margin-bottom: 0.9rem; }

/* ---------- Panels ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card);
    border: 1px solid var(--line) !important;
    border-radius: 20px !important;
    box-shadow: var(--shadow);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(62, 155, 79, 0.55) !important;
    box-shadow: 0 12px 32px rgba(62, 155, 79, 0.22);
}

/* ---------- Inputs ---------- */
label, div[data-testid="stWidgetLabel"] p {
    color: var(--forest) !important;
    font-weight: 600;
}
div[data-testid="stNumberInput"] > div > div {
    background: #ffffff;
    border: 1.5px solid rgba(62, 155, 79, 0.4);
    border-radius: 12px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stNumberInput"] > div > div:focus-within {
    border-color: var(--leaf);
    box-shadow: 0 0 0 3px rgba(123, 198, 90, 0.35);
}
div[data-testid="stNumberInput"] input {
    color: var(--forest);
    font-weight: 700;
    font-size: 1.05rem;
}
div[data-testid="stNumberInput"] button { background: transparent; color: var(--leaf); }
div[data-testid="stNumberInput"] button:hover { background: var(--mint); color: var(--forest); }

/* ---------- Voice recorder ---------- */
div[data-testid="stAudioInput"] {
    background: linear-gradient(135deg, var(--wheat-soft), #ffffff);
    border: 1.5px dashed rgba(232, 185, 49, 0.8);
    border-radius: 16px;
    padding: 0.4rem;
}

/* ---------- Alerts (warnings, transcription, errors) ---------- */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid var(--line);
}

/* ---------- Primary button ---------- */
div.stButton > button {
    width: 100%;
    padding: 0.9rem 1.2rem;
    border: none;
    border-radius: 16px;
    color: #ffffff;
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    background: linear-gradient(90deg, var(--leaf), var(--leaf-light));
    box-shadow: 0 8px 20px rgba(62, 155, 79, 0.38);
    transition: transform 0.15s ease, box-shadow 0.25s ease, filter 0.25s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.05);
    color: #ffffff;
    box-shadow: 0 12px 28px rgba(62, 155, 79, 0.5);
}
div.stButton > button:active { transform: translateY(0) scale(0.99); }
div.stButton > button:focus-visible { outline: 3px solid var(--wheat); outline-offset: 3px; }

/* ---------- Result card ---------- */
.result {
    padding: 1.6rem;
    margin-top: 1.4rem;
    border-radius: 22px;
    border: 2px solid var(--leaf-light);
    background: linear-gradient(135deg, #f1fadf, #ffffff 70%);
    box-shadow: var(--shadow);
    animation: grow 0.5s ease-out;
}
@keyframes grow {
    from { opacity: 0; transform: translateY(14px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
.result .tag { color: var(--moss); font-weight: 600; font-size: 0.9rem; }
.result .cond {
    font-family: 'Fraunces', serif;
    font-size: clamp(1.6rem, 4vw, 2.3rem);
    font-weight: 700;
    color: var(--leaf);
    margin: 0.15rem 0 1rem;
}
.meter-head {
    display: flex; justify-content: space-between; align-items: baseline;
    color: var(--moss); font-weight: 600; font-size: 0.92rem; margin-bottom: 0.4rem;
}
.meter-head b { font-family: 'Fraunces', serif; font-size: 1.55rem; color: var(--forest); }
.meter { height: 14px; border-radius: 99px; background: var(--soil-soft); overflow: hidden; }
.meter span {
    display: block; height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--wheat), var(--leaf-light), var(--leaf));
    animation: fill 0.9s ease-out;
}
@keyframes fill { from { width: 0; } }

.obs {
    margin-top: 1.2rem;
    padding: 0.9rem 1.1rem;
    border-radius: 14px;
    border-left: 4px solid var(--soil);
    background: var(--soil-soft);
    color: var(--forest);
}
.obs b { color: var(--soil); }

/* ---------- AI field explanation ---------- */
.ai-head { display: flex; align-items: center; gap: 0.9rem; margin: 1.6rem 0 0.8rem; }
.ai-badge {
    flex: 0 0 auto;
    width: 48px; height: 48px;
    display: grid; place-items: center;
    font-size: 1.4rem;
    border-radius: 16px;
    background: linear-gradient(145deg, var(--wheat-soft), #ffffff);
    border: 2px solid var(--wheat);
    box-shadow: 0 6px 16px rgba(232, 185, 49, 0.4);
}
.ai-head h3 {
    margin: 0;
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    color: var(--forest);
}
.ai-head small { display: block; color: var(--moss); font-size: 0.86rem; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) {
    border-color: rgba(232, 185, 49, 0.7) !important;
    border-left: 6px solid var(--wheat) !important;
    background: linear-gradient(135deg, #fffaf0, #ffffff);
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) p,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) li {
    color: var(--forest);
    line-height: 1.75;
    font-size: 1.02rem;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) strong { color: var(--soil); }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h1,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h2,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h3,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h4 {
    font-family: 'Fraunces', serif;
    color: var(--leaf);
}

div[data-testid="stSpinner"] { color: var(--leaf); }

/* ---------- Notices ---------- */
.notice {
    margin-top: 1.2rem;
    padding: 0.9rem 1.1rem;
    border-radius: 14px;
    border-left: 4px solid var(--sky);
    background: #e6f5fb;
    color: #1f5f78;
    font-size: 0.92rem;
}
.error-box {
    margin-top: 1.4rem;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    border: 1.5px solid #d9774a;
    background: #fdeee4;
    color: #8c3b17;
}

.foot { text-align: center; color: var(--moss); font-size: 0.84rem; margin-top: 2rem; }

/* ---------- Accessibility & mobile ---------- */
@media (max-width: 640px) {
    .hero { padding: 1.4rem 1.1rem 4rem; }
    .sprout { width: 54px; height: 54px; font-size: 1.7rem; }
    .sun { width: 100px; height: 100px; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="sun"></div>
        <div class="hero-row">
            <div class="sprout">🌱</div>
            <div>
                <h1>Crop Health Assistant</h1>
                <p>
                    AI-based agricultural decision support using crop, soil,
                    and environmental measurements.
                </p>
            </div>
        </div>
        <div class="chips">
            <span class="chip">🌤️ Climate</span>
            <span class="chip soil">🧪 Soil nutrients</span>
            <span class="chip gold">🎙️ Voice observation</span>
            <span class="chip">🤖 AI explanation</span>
        </div>
        <svg class="hills" viewBox="0 0 1200 90" preserveAspectRatio="none" aria-hidden="true">
            <path d="M0 55 Q200 15 400 50 T800 45 T1200 40 V90 H0Z" fill="#b6df8a"/>
            <path d="M0 70 Q250 35 500 68 T1000 62 T1200 66 V90 H0Z" fill="#7bc65a"/>
            <path d="M0 82 Q300 58 600 80 T1200 76 V90 H0Z" fill="#3e9b4f"/>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Field measurements
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.markdown(
        '<div class="section-title">📋 Enter Field Measurements</div>'
        '<div class="section-sub">Weather and soil conditions in your field</div>',
        unsafe_allow_html=True,
    )

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


st.write("")


# ---------------------------------------------------------------------------
# Soil nutrients
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.markdown(
        '<div class="section-title">🧪 Soil Nutrient Readings</div>'
        '<div class="section-sub">Nitrogen, phosphorus and potassium (NPK)</div>',
        unsafe_allow_html=True,
    )

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


st.write("")


# ---------------------------------------------------------------------------
# Voice observation
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.markdown(
        '<div class="section-title">🎙️ Field Observation</div>'
        '<div class="section-sub">'
        "You can describe what you observe in the crop or field using your voice."
        "</div>",
        unsafe_allow_html=True,
    )

    audio = st.audio_input("Record your field observation")

    voice_observation = ""

    if audio is not None:
        try:
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


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
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

        observation_html = ""

        if voice_observation:
            observation_html = f"""
                <div class="obs">
                    <b>🎙️ Field Observation</b><br>
                    {escape(voice_observation)}
                </div>
            """

        st.markdown(
            f"""
            <div class="result">
                <div class="tag">🌾 Crop Health Assessment</div>
                <div class="cond">Possible Condition: {escape(str(condition))}</div>
                <div class="meter-head">
                    <span>Model Confidence</span>
                    <b>{confidence:.2%}</b>
                </div>
                <div class="meter">
                    <span style="width: {max(0.0, min(float(confidence), 1.0)) * 100:.1f}%"></span>
                </div>
                {observation_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="ai-head">
                <div class="ai-badge">🤖</div>
                <div>
                    <h3>AI Field Explanation</h3>
                    <small>Plain-language advice based on your field readings</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown('<span class="ai-marker"></span>', unsafe_allow_html=True)

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

        st.markdown(
            """
            <div class="notice">
                This system provides agricultural decision support only.
                The result should be verified using field observations
                and professional agricultural advice.
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception as error:
        st.markdown(
            f'<div class="error-box">Error: {escape(str(error))}</div>',
            unsafe_allow_html=True,
        )


st.markdown(
    '<div class="foot">🌱 Crop Health Assistant · Agricultural decision support</div>',
    unsafe_allow_html=True,
)
