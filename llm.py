import os
import time

from langchain_openai import ChatOpenAI

PRIMARY_MODEL = "google/gemma-4-26b-a4b-it:free"
FALLBACK_MODELS = [
    "google/gemma-4-26b-a4b-it",
    "google/gemma-3-27b-it:free",
]


def create_llm():
    return ChatOpenAI(
        model=PRIMARY_MODEL,
        temperature=0.05,
        max_retries=0,
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:7860",
            "X-Title": "Diet Plan Generator",
        },
        extra_body={
            "models": FALLBACK_MODELS,
            "provider": {"allow_fallbacks": True},
        },
    )


def invoke_with_retry(llm, messages, retries=4):
    last_error = None
    for attempt in range(retries):
        try:
            return llm.invoke(messages)
        except Exception as error:
            last_error = error
            message = str(error).lower()
            if "429" not in message and "rate-limited" not in message:
                raise
            time.sleep(2 ** attempt)
    raise last_error
