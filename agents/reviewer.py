# agents/reviewer.py
from utils.llm import llm

def reviewer_critic(state):
    readme = state["readme"]
    feedback = llm.invoke(f"Point out missing or unclear parts in this README:\n{readme}")
    return {"review_feedback": feedback}
