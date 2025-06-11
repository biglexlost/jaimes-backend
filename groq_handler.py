import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "mixtral-8x7b-32768"  # You can also try "llama3-8b-8192"

async def generate_diagnosis(data):
    prompt = f"""
You are J.A.I.M.E.S., the Joint AI Mechanic Executive Specialist.

### INPUT FIELDS:
- Year: {data.get('year')}
- Make: {data.get('make')}
- Model: {data.get('model')}
- Mileage: {data.get('mileage')}
- VIN: {data.get('vin')}
- ZIP Code: {data.get('zip_code')}
- Problem Description: {data.get('symptoms')}
- When it started: {data.get('timeline')}
- Recent repairs/maintenance: {data.get('recent_work')}

### OUTPUT FORMAT:
<Diagnosis Summary>
- Vehicle: {data.get('year')} {data.get('make')} {data.get('model')}
- ZIP Code: {data.get('zip_code')}
- Symptoms: {data.get('symptoms')}
- Timeline: {data.get('timeline')}
- Most Likely Issue: [Your best guess]
- Suggested Repair: [What service or repair would be recommended]
- Confidence Level: High / Medium / Low
- Notes: [Any clarifications, alternate possibilities, or what else should be checked]
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

    result = response.json()

    # Debug: log the raw Groq result
    print("GROQ RAW RESPONSE:", result)

    # Smart fallback
    if "choices" in result and result["choices"]:
        return result["choices"][0]["message"]["content"]
    else:
        return f"Groq error: {result}"
