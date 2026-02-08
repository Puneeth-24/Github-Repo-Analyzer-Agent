from langchain_core.prompts import PromptTemplate


REPO_ANALYSIS_PROMPT = PromptTemplate.from_template("""
You are a senior software architect and code reviewer.

Analyze the following repository metadata:

{context}

Provide:

1. Project summary
2. Architecture overview
3. Tech stack explanation
4. How to run the project
5. Strengths
6. Suggested improvements

Write clearly and concisely.
""")