# 📘 GitHub README Improver (Multi-Agent System with Streamlit)

This app helps users improve their GitHub AI/ML project presentation by:
- Recommending better titles and summaries
- Suggesting metadata (tags, categories)
- Reviewing README clarity and completeness
- Verifying suggestions against actual repo content

## 👷‍♂️ Agents
- **Repo Analyzer**: Clones and extracts content/structure
- **Content Improver**: Suggests better titles/intros
- **Metadata Recommender**: Suggests tags/categories
- **Reviewer**: Identifies missing or unclear sections
- **Fact Checker**: Verifies suggestions against repo content

## 🚀 Usage
```bash
pip install -r requirements.txt
streamlit run main.py
```

Create a `.env` file with your OpenAI key:
```
OPENAI_API_KEY=your-key-here
```
