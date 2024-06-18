from openai import OpenAI

def generate_ai_response(inputText):
    client = OpenAI(
        base_url='http://172.20.10.9:11434/v1',  # Replace IP Address, keep 11434/v1
        api_key='ollama',  # Note: API key is required but unused in this snippet.
    )

    response = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{inputText}"},
        ]
    )

    return response.choices[0].message.content

#input = "Let's work together, what do you say?" # Input for response
#print(f"Loading response to ' {input} '... \n") # To view input and generate loading
#print(generate_ai_response(input)) # Output and test of model responses