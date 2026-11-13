import logging
import os
import time

import mlflow
import tiktoken
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.llm_client import SYSTEM_PROMPT, LLMClient

app = FastAPI()
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
mlflow.set_experiment("data790-chatbot")
mlflow.openai.autolog()
llm = LLMClient()
tokenizer = tiktoken.encoding_for_model(llm.model)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
	message: str

class ChatResponse(BaseModel):
	response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
	input_tokens = (len(tokenizer.encode(SYSTEM_PROMPT)) + len(tokenizer.encode(request.message)))

	if input_tokens >= 1000:
		raise HTTPException(status_code=413, detail="Input exceeds the 1000 token limit.")

	logger.info("Chat request received")

	start_time = time.perf_counter()

	try:
		response = llm.chat(request.message)
	except Exception:
		logger.exception("Chat request failed.")
		raise

	latency = time.perf_counter() - start_time

	logger.info("Chat response generated. Latency: %.2f seconds", latency)
	return ChatResponse(response=response)

@app.get("/health")
def health():
	return {"status": "running"}