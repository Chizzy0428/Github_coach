# agents/fact_checker.py
from utils.llm import llm

def fact_checker(state):
    structure = state["structure"]
    suggestions = (
        state.get("improved_content", "") + "\n" +
        state.get("review_feedback", "")
    )
    verified = llm.invoke(
        f"Based on the repo structure below, check whether these suggestions are valid:\n"
        f"=== STRUCTURE ===\n{structure}\n=== SUGGESTIONS ===\n{suggestions}"
    )
    return {"verified_suggestions": verified}
