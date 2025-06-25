from fastapi import FastAPI, Request
from groq_handler import generate_diagnosis

app = FastAPI()

# ✅ Add a friendly root route so the base URL isn't 404
@app.get("/")
async def root():
    return {
        "message": "JAIMES backend is live and ready to diagnose 🚗🛠️",
        "usage": "POST JSON to /intake with vehicle data"
    }

# 🔧 Your existing POST route
@app.post("/intake")
async def intake(request: Request):
    data = await request.json()
    response = await generate_diagnosis(data)
    return {"result": response}
