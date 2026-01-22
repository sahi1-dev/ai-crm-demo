from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph

app = FastAPI()

# ----------- Request Model -----------

class Interaction(BaseModel):
    text: str

# ----------- 5 LANGGRAPH TOOLS (STATE MERGING FIXED) -----------

def extract_doctor(state):
    state["doctor"] = "Dr. Sharma"
    return state

def extract_topic(state):
    state["topic"] = "Product X"
    return state

def extract_sentiment(state):
    state["sentiment"] = "Positive"
    return state

def extract_followup(state):
    state["follow_up"] = "Call again in 2 weeks"
    return state

def final_assembler(state):
    return {
        "doctor": state.get("doctor"),
        "topic": state.get("topic"),
        "sentiment": state.get("sentiment"),
        "follow_up": state.get("follow_up"),
        "raw_text": state.get("text")
    }

# ----------- LANGGRAPH WORKFLOW -----------

graph = StateGraph(dict)

graph.add_node("extract_doctor", extract_doctor)
graph.add_node("extract_topic", extract_topic)
graph.add_node("extract_sentiment", extract_sentiment)
graph.add_node("extract_followup", extract_followup)
graph.add_node("final_assembler", final_assembler)

graph.set_entry_point("extract_doctor")
graph.add_edge("extract_doctor", "extract_topic")
graph.add_edge("extract_topic", "extract_sentiment")
graph.add_edge("extract_sentiment", "extract_followup")
graph.add_edge("extract_followup", "final_assembler")

agent = graph.compile()

# ----------- API ENDPOINT -----------

@app.post("/log-interaction")
def log_interaction(interaction: Interaction):
    # IMPORTANT: start state with text included
    initial_state = {"text": interaction.text}
    result = agent.invoke(initial_state)
    return result
