from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    # Your local model name from 'ollama list'
    model="deepseek-r1:1.5b",
    base_url="http://192.168.1.5:11434/v1",
    # API key is required by the library but ignored by Ollama
    api_key="ollama",     
    temperature=0.1
)

for chunk in llm.stream("Why is the sky blue?"):
    # Print the content of the chunk immediately
    # end='' prevents newlines between chunks
    # flush=True forces Python to print it instantly instead of buffering
    print(chunk.content, end='', flush=True)