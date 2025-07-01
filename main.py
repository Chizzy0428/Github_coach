import streamlit as st
from langgraph.graph import StateGraph, END
from agents.repo_analyzer import repo_analyzer
from agents.content_improver import content_improver
from agents.metadata_recommender import metadata_recommender
from agents.reviewer import reviewer_critic
from agents.fact_checker import fact_checker
from typing import TypedDict, Optional


# Define state structure
class State(TypedDict, total=False):
    repo_url: str
    description: Optional[str]
    readme: str
    structure: str
    improved_content: str
    tags: str
    review_feedback: str
    verified_suggestions: str


# Create the agent workflow graph
def create_graph():
    workflow = StateGraph(State)

    workflow.add_node("Repo Analyzer", repo_analyzer)
    workflow.add_node("Content Improver", content_improver)
    workflow.add_node("Metadata Recommender", metadata_recommender)
    workflow.add_node("Reviewer", reviewer_critic)
    workflow.add_node("Fact Checker", fact_checker)

    workflow.set_entry_point("Repo Analyzer")
    workflow.add_edge("Repo Analyzer", "Content Improver")
    workflow.add_edge("Repo Analyzer", "Metadata Recommender")
    workflow.add_edge("Repo Analyzer", "Reviewer")
    workflow.add_edge("Reviewer", "Fact Checker")
    workflow.add_edge("Fact Checker", END)

    return workflow.compile()


# ---------- Streamlit UI ----------
st.set_page_config(page_title="GitHub README Improver", layout="wide")
st.title("GitHub Publication Assistant")
st.markdown("This multi‑agent system helps enhance the presentation of your AI/ML GitHub projects.")

repo_url = st.text_input("Enter GitHub Repository URL")
description = st.text_area("Optional: Add a short project description")

if st.button("Analyze and Improve") and repo_url:
    graph = create_graph()
    state = {"repo_url": repo_url, "description": description}
    result = graph.invoke(state)

    # Extract content safely
    def extract_text(obj):
        return obj.content if hasattr(obj, "content") else str(obj)

    st.subheader("Verified Suggestions")
    st.markdown(extract_text(result.get("verified_suggestions", "No suggestions generated.")))

    st.subheader("Metadata Tags")
    tags_raw = extract_text(result.get("tags", "No tags suggested."))
    tags = [t.strip("# ") for t in tags_raw.split() if t.startswith("#")]
    st.markdown(", ".join(tags) if tags else tags_raw)

    st.subheader("✍Improved Title & Intro")
    st.markdown(extract_text(result.get("improved_content", "No improvement suggestions.")))

    st.subheader("Review Feedback")
    st.markdown(extract_text(result.get("review_feedback", "No review feedback.")))
