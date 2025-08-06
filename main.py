from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import asyncio
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

@app.post("/v1/chat/completions")
@app.post("/v1/chat/completions/")
async def chat_completions(request: Request):
    body = await request.json()
    stream = body.get("stream", False)
    if not stream:
        # Non-streaming fallback (just for safety)
        return {
            "id": "chatcmpl-dummy",
            "object": "chat.completion",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello! This is a dummy response."
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 5,
                "total_tokens": 10
            }
        }
    # Streaming response for Anam compatibility
    async def event_stream():
        chunks = ["Hello", " there,", " how", " can", " I", " help", " you?"]
        for chunk in chunks:
            data = {
                "choices": [
                    {
                        "delta": {"content": chunk},
                        "index": 0,
                        "finish_reason": None
                    }
                ]
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0.2)  # simulate delay
        yield "data: [DONE]\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
