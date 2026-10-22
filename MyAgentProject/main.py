

from graph import chatbot


def ask_hexbot(question: str) -> str:
    """
    Send a user question to the LangGraph chatbot.
    """
    result = chatbot.invoke({
        "question": question
    })

    return result["answer"]


if __name__ == "__main__":
    print("HEXBot")
    print("=" * 40)

    while True:
        question = input("\nYou: ")

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        answer = ask_hexbot(question)

        print(f"\nHEXBot: {answer}")