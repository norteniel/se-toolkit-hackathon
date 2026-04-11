from fastapi import FastAPI
from pydantic import BaseModel
import random

from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()
history = []

class Options(BaseModel):
    items: list[str]

@app.post("/choose")
def choose(options: Options):
    if len(options.items) < 2:
        return {"error": "Need at least 2 options"}

    choice = random.choice(options.items)

    explanation = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": f"Why is '{choice}' a good choice among {options.items}?"}
        ]
    )

    history.append(options.items)

    return {
        "result": f"I choose: {choice}",
        "explanation": explanation.choices[0].message.content,
        "history": history
    }