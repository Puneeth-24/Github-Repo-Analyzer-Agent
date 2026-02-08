import json

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

from agent.prompts import REPO_ANALYSIS_PROMPT


class LLMReasonerError(Exception):
    pass


def summarize_context(context: dict) -> dict:
    """
    Reduce context size before sending to LLM.
    """
    return {
        "repo_name": context["repo_name"],
        "primary_language": context["primary_language"],
        "frameworks": context["frameworks"],
        "repo_type": context["repo_type"],
        "important_files": context["important_files"],
        "entry_points": context["entry_points"],
        "stats": context["stats"],
    }


def build_chain():
    """
    Create LangChain pipeline using Ollama.
    """

    llm = ChatOllama(
        model="llama3.2",
        temperature=0.3,
    )

    parser = StrOutputParser()

    chain = RunnableSequence(
        REPO_ANALYSIS_PROMPT,
        llm,
        parser,
    )

    return chain


def analyze_repo(context: dict) -> str:
    """
    Run repo analysis through LangChain + Ollama.
    """

    print("🧠 Running local Ollama analysis...")

    try:
        reduced_context = summarize_context(context)

        chain = build_chain()

        result = chain.invoke({
            "context": json.dumps(reduced_context, indent=2)
        })

        print("✅ Analysis complete")

        return result

    except Exception as e:
        raise LLMReasonerError(f"Ollama analysis failed: {e}")