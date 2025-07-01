from langchain_openai import ChatOpenAI
import streamlit as st

# Access secrets from Streamlit
openai_api_key = st.secrets["OPENAI_API_KEY"]
model_name = st.secrets.get("OPENAI_MODEL", "gpt-3.5-turbo")

# Initialize the LLM
llm = ChatOpenAI(model=model_name, api_key=openai_api_key)

