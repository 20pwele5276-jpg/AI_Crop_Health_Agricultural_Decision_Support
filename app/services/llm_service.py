import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def explain_condition(
    condition,
    temperature,
    humidity,
    soil_moisture,
    soil_ph,
    nitrogen,
    phosphorus,
    potassium,
    voice_observation="",
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "LLM explanation is unavailable because the API key is not configured."

    client = Groq(api_key=api_key)

    observation_text = voice_observation or "No additional field observation provided."

    prompt = f"""
You are an agricultural decision-support assistant.

A machine learning model detected this possible crop health condition:

Condition: {condition}
Temperature: {temperature} °C
Humidity: {humidity} %
Soil Moisture: {soil_moisture} %
Soil pH: {soil_ph}
Nitrogen: {nitrogen}
Phosphorus: {phosphorus}
Potassium: {potassium}

Additional observation from the farmer:
{observation_text}

Explain the result in simple language for a farmer or non-technical person.

Include:
1. What the possible condition means
2. Why the readings may indicate it
3. What the farmer should check or consider doing

Keep the explanation short, practical, and easy to understand.

Do not say that the condition is confirmed.
Do not provide dangerous or highly specific chemical treatment instructions.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        reasoning_effort="low",
    )

    return response.choices[0].message.content