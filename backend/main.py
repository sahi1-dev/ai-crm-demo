from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # 👈 ADD THIS
from pydantic import BaseModel
from langgraph.graph import StateGraph

app = FastAPI()

# 👇 ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React ko allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Interaction(BaseModel):
    text: str

# ---------- AI TOOL ----------
def log_interaction_tool(state):
    text = state["text"].lower()

    doctor = "Unknown Doctor"
    topic = "Unknown Topic"
    sentiment = "Neutral"
    follow_up = "No follow-up"

    if "sharma" in text:
        doctor = "Dr. Sharma"
    if "product" in text or "x" in text:
        topic = "Product X"
    if "good" in text or "positive" in text:
        sentiment = "Positive"
    if "bad" in text or "negative" in text:
        sentiment = "Negative"
    if "follow" in text or "call" in text:
        follow_up = "Call again in 2 weeks"

    return {
        "doctor": doctor,
        "topic": topic,
        "sentiment": sentiment,
        "follow_up": follow_up,
        "raw_text": state["text"]
    }


# ---------- LANGGRAPH AGENT ----------
graph = StateGraph(state_schema=dict)   # 👈 small fix here
graph.add_node("log_interaction", log_interaction_tool)
graph.set_entry_point("log_interaction")
agent = graph.compile()

# ---------- API ----------
@app.post("/log-interaction")
def log_interaction(interaction: Interaction):
    result = agent.invoke({"text": interaction.text})
    return result
