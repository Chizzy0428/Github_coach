# agents/content_improver.py
from utils.llm import llm

def content_improver(state):
    readme = state["readme"]
    suggestion = llm.invoke(f"Improve title and intro for this README:\n{readme}")
    return {"improved_content": suggestion}   # <-- only new field
