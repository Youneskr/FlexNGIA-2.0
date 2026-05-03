# Test whether the LLM is working (considers the configuration provided in .env)
#~/Desktop/FlexNGIA-2.0/cc-agent$ sudo agent/venv/bin/python agent/testLLM.py
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()


def load_llm():
    provider = os.getenv("LLM_PROVIDER", "GROQ").upper()
    model = os.getenv("LLM_MODEL")
    temperature = float(os.getenv("LLM_TEMPERATURE", 0))

    if provider == "GROQ":
        return ChatGroq(
            model=model,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=temperature,
        )
    elif provider == "GEMINI":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=temperature,
        )
    elif provider == "OPENAI":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
        )
    elif provider == "OPENROUTER":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
        )
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")


def main():
    print("[Test] Checking LLM access...\n")

    try:
        llm = load_llm()
        response = llm.invoke("Say hello")

        # Print only the content
        print("LLM Response:")
        print(response.content)
        print()

        # Status message
        if response.content and len(response.content.strip()) > 0:
            print("[SUCCESS] LLM is working correctly ✅")
        else:
            print("[WARNING] LLM responded but content is empty ⚠️")

    except Exception as e:
        print("[ERROR] LLM is NOT working ❌")
        print("Reason:", e)


if __name__ == "__main__":
    main()
