# agents/metadata_recommender.py
from utils.llm import llm

def metadata_recommender(state):
    readme = state["readme"]
    tags = llm.invoke(f"Suggest relevant tags for:\n{readme}")
    return {"tags": tags}
