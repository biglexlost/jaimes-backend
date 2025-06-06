from fastapi import FastAPI, Request
from groq_handler import generate_diagnosis

app = FastAPI()

@app.post("/intake")
async def intake(request: Request):
    data = await request.json()
    response = await generate_diagnosis(data)
    return {"result": response}