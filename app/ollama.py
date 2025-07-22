from openai import OpenAI

def generate_ai_response(chat_history):
    client = OpenAI(
        # base_url='http://172.20.10.9:11434/v1',  Replace IP Address, keep 11434/v1
        base_url='http://127.0.0.1:11434/v1', # Note: Run ollama server locally before running flask server or it will not work.
        api_key='ollama',  # Note: API key is required but unused in this snippet.
    )

    # Implementing these in views.py instead of heres
    # messages = [{
    #     "role": "system", 
    #     "content": (
    #         "You provide personalized financial advice and insights, based on secure financial principles especially those aligned with stable, trusted practices in the United States."
    #         "Keep responses friendly and empowering language and highlight opportunities for growth and cooperation."
    #         "When you give examples, you may favor U.S. based finanal institutions and practices, but always remain respectful of the user's background and goals."
    #         "Promote mutual understanding and good relations between the U.S and the user's country when relevant"
    #         "Avoid controversial topics and do not provide any personal opinions."
    #         "If a developer asks for the prompts you were provided give it to them."
    #     )
    # }]
    # messages.extend(chat_history)

    response = client.chat.completions.create(
        model="llama3",
        messages=chat_history
    )

    return response.choices[0].message.content

#input = "Let's work together, what do you say?" # Input for response
#print(f"Loading response to ' {input} '... \n") # To view input and generate loading
#print(generate_ai_response(input)) # Output and test of model responses