import streamlit as st
import time
from langgraph.graph import StateGraph, END
from agents.repo_analyzer import repo_analyzer
from agents.content_improver import content_improver
from agents.metadata_recommender import metadata_recommender
from agents.reviewer import reviewer_critic
from agents.fact_checker import fact_checker
from typing import TypedDict, Optional


# ---------- Define State Structure ----------
class State(TypedDict, total=False):
    repo_url: str
    description: Optional[str]
    readme: str
    structure: str
    improved_content: str
    tags: str
    review_feedback: str
    verified_suggestions: str
    runtime: float


# ---------- Multi-Agent Workflow ----------
def create_graph():
    workflow = StateGraph(State)

    # Specialized AI Agents
    workflow.add_node("Repo Analyzer", repo_analyzer)              # Extracts README and repo structure
    workflow.add_node("Content Improver", content_improver)        # Refines title & intro
    workflow.add_node("Metadata Recommender", metadata_recommender) # Generates tags
    workflow.add_node("Reviewer", reviewer_critic)                 # Audits tone, clarity, structure
    workflow.add_node("Fact Checker", fact_checker)                # Validates reviewer outputs

    # Workflow logic
    workflow.set_entry_point("Repo Analyzer")
    workflow.add_edge("Repo Analyzer", "Content Improver")
    workflow.add_edge("Repo Analyzer", "Metadata Recommender")
    workflow.add_edge("Repo Analyzer", "Reviewer")
    workflow.add_edge("Reviewer", "Fact Checker")
    workflow.add_edge("Fact Checker", END)

    return workflow.compile()


# ---------- Streamlit UI ----------
st.set_page_config(page_title="GitHub README Improver", layout="wide")
st.title("🤖 GitHub Publication Assistant")
st.markdown("A multi-agent system that analyzes and enhances your GitHub AI/ML project presentation using LLM-powered assistants.")

repo_url = st.text_input("🔗 Enter GitHub Repository URL")
description = st.text_area("📝 Optional: Add a short project description")

if st.button("🔍 Analyze and Improve") and repo_url:
    start_time = time.time()
    graph = create_graph()
    state = {"repo_url": repo_url, "description": description}
    result = graph.invoke(state)
    end_time = time.time()
    result["runtime"] = round(end_time - start_time, 2)

    # ---------- Safe Extraction ----------
    def extract_text(obj):
        return obj.content if hasattr(obj, "content") else str(obj)

    # ---------- Display Results ----------
    st.subheader("✅ Verified Suggestions")
    st.markdown(extract_text(result.get("verified_suggestions", "No suggestions generated.")))

    st.subheader("🏷️ Metadata Tags")
    tags_raw = extract_text(result.get("tags", "No tags suggested."))
    tags = [t.strip("# ") for t in tags_raw.split() if t.startswith("#")]
    st.markdown(", ".join(tags) if tags else tags_raw)

    st.subheader("✍ Improved Title & Intro")
    st.markdown(extract_text(result.get("improved_content", "No improvement suggestions.")))

    st.subheader("🔍 Review Feedback")
    st.markdown(extract_text(result.get("review_feedback", "No review feedback.")))

    st.info(f"🕒 Processing Time: {result['runtime']} seconds")


# ---------- Expandable Info ----------
with st.expander("📘 Project Architecture & Agent Roles"):
    st.markdown("""
    **🧠 Agents:**
    - **Repo Analyzer**: Clones repo and extracts README content and project structure.
    - **Content Improver**: Suggests a clearer project title and summary introduction.
    - **Metadata Recommender**: Generates project-related tags for discoverability.
    - **Reviewer**: Provides feedback on tone, structure, and completeness of the README.
    - **Fact Checker**: Validates reviewer feedback and filters unsupported claims.

    **🛠️ Features:**
    - Modular LangGraph-based agent system
    - Human-in-the-loop design pattern
    - Performance logging (runtime)
    - LLM-powered recommendations

    **🚀 Run Instructions:**
    ```
    pip install -r requirements.txt
    streamlit run main.py
    ```

    ✅ Ensure you have an `.env` file with:
    ```
    OPENAI_API_KEY=your-key-here
    ```
    """)

