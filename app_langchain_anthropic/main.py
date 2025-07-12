import uvicorn
from fastapi import FastAPI, HTTPException
from app_langchain_anthropic.langchain_pipeline import generate_response
from app.model.ChatResponse import ChatResponse
from app.model.ChatRequest import ChatRequest

app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = generate_response(request.message)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
