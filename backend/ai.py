from ollama import chat

role = "You are an assistant. Be as savage as you want to, but still answer the question. You could also be an anime tsundere"


def res(input):
    response = chat(
        model='free01/gemma4:e4b',
        messages=[{'role': 'user', 'content': f"{role} Here is your input {input}"}]
    )
    print(response.message.content)
    return response.message.content   


