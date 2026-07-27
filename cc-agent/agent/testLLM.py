# Test whether the configured LLM is working (uses the configuration in .env)
#
# Usage:
#   cd ~/Desktop/FlexNGIA-2.0/cc-agent
#   sudo agent/venv/bin/python agent/testLLM.py

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv("config.env")


def get_response_text(response):
    """Extract plain text from a LangChain AIMessage."""

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()

    return str(content).strip()


def load_llm():
    """Load the LLM configured in the .env file."""

    provider = os.getenv("LLM_PROVIDER", "GROQ").strip().upper()
    model = os.getenv("LLM_MODEL", "").strip()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0"))

    if not model:
        raise ValueError("LLM_MODEL is not defined in the .env file.")

    if provider == "GROQ":
        api_key = os.getenv("GROQ_API_KEY")
    elif provider == "GEMINI":
        api_key = os.getenv("GEMINI_API_KEY")
    elif provider == "OPENAI":
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider == "OPENROUTER":
        api_key = os.getenv("OPENROUTER_API_KEY")
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    # Mask the API key for display
    if api_key:
        masked_key = f"{api_key[:8]}...{api_key[-4:]}"
    else:
        masked_key = "<NOT SET>"

    print("=== LLM Configuration ===")
    print(f"Provider    : {provider}")
    print(f"Model       : {model}")
    print(f"Temperature : {temperature}")
    print(f"API Key     : {masked_key}")
    print("=========================\n")

    if provider == "GROQ":
        return ChatGroq(
            model=model,
            groq_api_key=api_key,
            temperature=temperature,
        )

    elif provider == "GEMINI":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
        )

    elif provider == "OPENAI":
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=temperature,
        )

    elif provider == "OPENROUTER":
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


def main():
    print("[TEST] Checking LLM access...\n")

    try:
        llm = load_llm()

        print("Sending request to the LLM...\n")

        response = llm.invoke("Say hello.")

        text = get_response_text(response)

        print("=== LLM Response ===")
        print(text)
        print("====================\n")

        if text:
            print("[SUCCESS] LLM is reachable and responding correctly. ✅")
        else:
            print("[WARNING] LLM responded but returned empty content. ⚠️")

    except Exception as e:
        print("[ERROR] LLM is NOT working. ❌")
        print(f"Reason: {e}\n")
        print("You can modify the LLM configuration by editing the 'agent/.env' file.")
        print("This includes the LLM provider, model, temperature, and API key.\n\n")
        print("If you do not already have an API key, you can create one from one of the following providers:")
        print(f"  • Groq:          https://console.groq.com/keys")          
        print(f"  • OpenAI:       https://platform.openai.com/api-keys")   
        print(f"  • Google Gemini:https://aistudio.google.com/app/apikey")  
                 

if __name__ == "__main__":
    main()
