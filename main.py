from fastapi import FastAPI, Request, Response
from groq_handler import generate_diagnosis

app = FastAPI()

# ✅ Add a friendly root route so the base URL isn't 404
@app.get("/")
async def root():
    return {"status": "JAIMES backend alive!"}

@app.head("/")
async def head_root():
    return Response(status_code=200)
    
@app.post("/chat/completions")
async def chat_completions(request: Request):
    payload = await request.json()
    # assuming payload has the shape your handler expects:
    result = await generate_diagnosis(payload)
    return result
    
