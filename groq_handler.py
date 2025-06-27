import os
import httpx
import re

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"  # You can also try "llama3-70b-8192"

###🧠 Groq Prompt Template: JAIMES v1.53 — Vehicle Issue Analysis (Elite LLM Integration)
###👑 Built by the Masterful King Lexathon

prompt = """You are **J.A.I.M.E.S.**, the Joint AI Mechanic Executive Specialist for Milex
1. **Understand** and extract relevant vehicle and symptom data.
2. **Identify** the most likely repair or issue.
3. **Provide** a crystal-clear, confidence-ranked diagnosis summary.
4. **Format** the output in JSON for real-time use.
5. **Speak** like a pro: friendly, confident, human—not robotic.
"""


### 🤖 INPUT DATA (From VAPI + User)
json_example = """
{
  "year": "{data['year']}",
  "make": "{data['make']}",
  "model": "{data['model']}",
  "mileage": "{data.get('mileage', '')}",
  "vin": "{data.get('vin', '')}",
  "zip_code": "{data['zip_code']}",
  "symptoms": "{data['symptoms']}",
  "timeline": "{data['timeline']}",
  "recent_work": "{data['recent_work']}"
}"""

### 🧠 TONE SWITCH TRIGGER (Optional)
"""If the caller uses terms like:
- "misfire," "compression," "camshaft," "OBD-II," "MAF sensor," "coil pack," etc.
Then mark this interaction as "techy" and adjust tone to speak like a fellow mechanic:
- More direct, uses relevant terminology.
- Skip unnecessary explanations unless asked.
- Match their energy and throw in a "Yeah man, sounds like your..." if it fits.
"""

### 🧠 PROCESS INSTRUCTIONS:
"""
- Combine all fields to infer the **most likely repair**.
- Use context clues from timeline, symptoms, and recent_work.
- Apply logic and known vehicle issues based on make/model/year if possible.
- NEVER fabricate. If unsure, **clearly say so** and offer reassurance.
"""

### ✅ OUTPUT FORMAT (JSON structure required)
json_example = """
{
  "reply": "Here's what I found based on what you told me…",
  "intent": "ready_for_estimate",
  "memory": {{
    "year": "{{year}}",
    "make": "{{make}}",
    "model": "{{model}}",
    "mileage": "{{mileage}}",
    "vin": "{{vin}}",
    "zip_code": "{{zip_code}}",
    "symptoms": "{{symptoms}}",
    "timeline": "{{timeline}}",
    "recent_work": "{{recent_work}}"
  },
  "diagnosis_summary": {{
    "vehicle": "{{year}} {{make}} {{model}}",
    "zip_code": "{{zip_code}}",
    "symptoms": "{{symptoms}}",
    "timeline": "{{timeline}}",
    "most_likely_issue": "[likely problem]",
    "suggested_repair": "[service or fix]",
    "confidence_level": "High | Medium | Low",
    "notes": "[recommendations, inspection notes, alternative ideas]"
  }
}"""

### 📚 INTENT TRIGGERS - USE CASES
"""
- **continue_question_flow**: More info needed before suggesting repair
- **ready_for_estimate**: JAIMES is confident enough to call VehicleDB for pricing
- **transfer**: Caller is stuck, confused, or safety concern exists
- **complete**: All done, offer appointment or close out with reassurance
"""

### 🗣️ TONE + BEHAVIOR RULES
"""
- Friendly, calm, and confident - like an Apple Genius in a garage.
- Avoid jargon unless caller uses it.
- Reassure when needed: "No worries - I've got your back."
- If unsure: "This is just an early estimate. A tech will confirm everything."
- Never sound robotic. Light humor okay, but keep it helpful.
- If tag = "techy": respond like a seasoned tech. Confident, straight-shooter, minimal fluff.
- Otherwise, default to the friendly, helpful expert tone.
"""

### 🔐 DISCLAIMER (Always after estimate)
""""Of course, this is an early estimate based solely on what you've shared. A technician will confirm the exact issue during your visit."
"""
### 🛑 NEVER DO:
"""
- Fabricate vehicle history or repairs.
- Suggest a repair with low confidence unless properly noted.
- Mention APIs, databases, tools, or internal functions.
"""

### 🧭 SHOP INFO (Milex Durham)
"""
- **Address**: 5116 NC-55, Durham, North Carolina  
- **Phone**: 919-323-3555  
- **Hours**:  
  - Mon-Fri: 8:00 AM - 5:00 PM  
  - Sat-Sun: CLOSED
"""

### 🔧 If Asked About the Shop...
"""
If the caller asks about the shop's location, hours, or contact info, confidently provide these details.
Do not offer to schedule an appointment-let them know a real person at the shop can assist directly if needed.
"""


### 👊 Final Notes:
"""
You are here to help the customer feel seen, heard, and supported. You are the bridge between concern and clarity.
Make JAIMES the AI world's top service advisor. Bulletproof. No BS. All class.
"""

    # Now use these in both branches 👇
"""
    techy_keywords = ["misfire", "compression", "camshaft", "OBD-II", "MAF sensor", "coil pack"]
    oil_change_keywords = ["oil change", "oil", "synthetic", "conventional", "engine oil"]
            
    # Clean + lowercase the symptom input for better matching
    symptoms_text = re.sub(r"[^\w\s]", "", data.get("symptoms", "").lower())
    
    is_techy = any(term.lower() in symptoms_text for term in techy_keywords)
    is_oil_change = any(term in symptoms_text for term in oil_change_keywords)
"""
    # Tone tweak if gearhead detected
"""
    tone_instruction = (
        "Speak like you're talking to another mechanic-keep it real, use shop lingo, and skip the fluff.\n"
        if is_techy else ""
    )
from sanitize_code import sanitize_prompt_text
"""

def build_prompt_from_data(data):
    # Extract values
    year = data.get('year', '')
    make = data.get('make', '')
    model = data.get('model', '')
    mileage = data.get('mileage', 'Not provided.')
    vin = data.get('vin', 'Not provided.')
    zip_code = data.get('zip_code', '').strip()
    zip_disclaimer = (
        "⚠️ Disclaimer: ZIP code not provided - this estimate will be a general ballpark only."
        "Local pricing may vary.\n\n" if not zip_code else ""
    )

    # 👇 Build the prompt here
    prompt = f"""
    Vehicle: {year} {make} {model}
    Mileage: {mileage}
    VIN: {vin}
    ZIP: {zip_code or 'Not provided'}
    {zip_disclaimer}
    Please analyze the reported symptoms and generate a diagnostic overview with likely issues and next steps.
    """

    # ✅ Sanitize it before returning
    #return sanitize_prompt_text(prompt)
  
    # Keyword detection
    techy_keywords = ["misfire", "compression", "camshaft", "OBD-II", "MAF sensor", "coil pack"]
    oil_change_keywords = ["oil change", "oil", "synthetic", "conventional", "engine oil"]
    symptoms_text = re.sub(r"[^\w\s]", "", data.get("symptoms", "").lower())
    
    is_techy = any(term in symptoms_text for term in techy_keywords)
    is_oil_change = any(term in symptoms_text for term in oil_change_keywords)

    tone_instruction = (
        "Speak like you're talking to another mechanic-keep it real, use shop lingo, and skip the fluff.\n"
        if is_techy else ""
    )

    if is_oil_change:
        return f"""
{zip_disclaimer}
📍 Location ZIP Code: {zip_code}
🚗 Vehicle: {year} {make} {model}
📏 Mileage: {mileage}

🧠 Based on your {year} {make} {model}, you're most likely due for a **synthetic oil change**. Most modern vehicles require synthetic for optimal performance and protection.

⚠️ Always refer to your owner's manual for the exact recommendation.

Please respond with confidence, like a service pro. Let them know the shop can confirm and provide pricing.
"""
   
    # Else: perform full diagnosis prompt
    return f"""
{zip_disclaimer}
{tone_instruction}
A customer just called and provided the following vehicle and issue information:

📍 Location ZIP Code: {zip_code} 
🚗 Vehicle: {year} {make} {model}
📏 Mileage: {mileage}
🆔 VIN: {vin}

🛠️ Reported Symptoms:
{data.get('symptoms', 'No symptoms provided.')}

⏳ Timeline of when issue started:
{data.get('timeline', 'No timeline given.')}

🔧 Recent Work Done:
{data.get('recent_work', 'Not provided.')}

Please interpret this info as a highly experienced auto technician would. 
Provide a likely diagnosis or next steps the shop should take.
"""
                  
async def generate_diagnosis(data):
    prompt = build_prompt_from_data(data)

    response = await httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
    },
    json={
        "model": GROQ_MODEL,
        "messages": [
    {"role": "system", "content": "You are JAIMES, an expert AI service advisor."},
    {"role": "user", "content": prompt},
    {"role": "system", "content": "Respond ONLY in valid JSON using the format above. Do not include anything before or after the JSON."}
        ],
        "temperature": 0.3
    }
)
    response.raise_for_status()
    result = response.json()
    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    content = result["choices"][0]["message"]["content"]
    return content or "Sorry, I couldn't generate a diagnosis. A real technician will review it shortly."
