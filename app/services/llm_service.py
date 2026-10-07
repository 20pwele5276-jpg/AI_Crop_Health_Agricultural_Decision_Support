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

A machine learning system detected this possible crop health condition:

Condition: {condition}
Temperature: {temperature} °C
Humidity: {humidity} %
Soil Moisture: {soil_moisture} %
Soil pH: {soil_ph}
Nitrogen: {nitrogen}
Phosphorus: {phosphorus}
Potassium: {potassium}

Additional field observation from the farmer:
{observation_text}

Explain this result in very simple language for a farmer or non-technical person.

Give:
1. What this condition means
2. Why these readings and observations may indicate it
3. What the farmer should check or consider doing

Keep the explanation short and practical.

Do not claim that the condition is confirmed.
Do not provide dangerous or highly specific chemical treatment instructions.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content