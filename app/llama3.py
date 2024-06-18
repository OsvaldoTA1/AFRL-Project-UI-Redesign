from openai import OpenAI
import csv

def queryLlama3(inputText):
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

    print(response)
    LLMOut = response.choices[0].message.content

    return LLMOut


def save_response_to_csv(input_query, model_response, filename='responses.csv'):
    # Define the CSV file header
    fieldnames = ['Input Query', 'Model Response']

    # Write the responses to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Input Query': input_query, 'Model Response': model_response})


def main():
    print("In Progress...")
    inputText = "Sample text"  # Update text as needed
    response = queryLlama3(inputText)

    if response:
        # Save the collected response to a CSV file
        save_response_to_csv(inputText, response)

if __name__ == "__main__":
    main()