


from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.7
)


def ask_ai(message):
    response = llm.invoke(message)
    return response.content


if __name__ == "__main__":
    answer = ask_ai("Hello! Introduce yourself as HEXBot.")
    print(answer)