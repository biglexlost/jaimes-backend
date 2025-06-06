import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "mixtral-8x7b-32768"

async def generate_diagnosis(data):
    prompt = f"""You are J.A.I.M.E.S., the Joint AI Mechanic Executive Specialist.

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

If the data is inconsistent or unclear, do NOT fabricate. Instead, respond like this:
"Thanks for the info. Based on what you've shared, I can't confidently determine the issue without a professional inspection. I’d still like to give you a rough direction, so here’s what I *think* might be going on..."
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
        res = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        return res.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")