import os
import dotenv
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, Header
from pydantic import BaseModel
from .main import load_model, generate_response

dotenv.load_dotenv()

app = FastAPI()

tokenizer, model = None, None
REQUIRED_TOKEN = os.environ.get("CHAT_BOT_TOKEN")

class ChatRequest(BaseModel):
    input: str
    max_new_tokens: int = 500

@app.on_event("startup")
def startup_event():
    global tokenizer, model
    tokenizer, model = load_model()

def check_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="缺少或错误的Token")
    token = authorization.split(" ", 1)[1]
    if token != REQUIRED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token无效")

@app.post("/chat")
async def chat_endpoint(req: ChatRequest, authorization: str = Header(None)):
    check_token(authorization)
    if tokenizer is None or model is None:
        return {"error": "模型未加载"}
    response = generate_response(tokenizer, model, req.input, req.max_new_tokens)
    return {"response": response}

def main():
    uvicorn.run("chat_bot_model.server:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main() 