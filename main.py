from fastapi import FastAPI
from pydantic import BaseModel
import random

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Options(BaseModel):
    items: list[str]

@app.post("/choose")
def choose(options: Options):
    if len(options.items) < 2:
        return {"error": "Need at least 2 options"}

    choice = random.choice(options.items)
    return {"result": f"I choose: {choice}"}