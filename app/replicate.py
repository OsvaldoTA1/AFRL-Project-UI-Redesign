import replicate
import cred

API_TOKEN = getattr(cred, 'REPLICATE_API_TOKEN', None)
client = None

# Initialize the Replicate client with the API token if it exists
if API_TOKEN:
    # If it's a valid token, initialize the client
    try:
        client = replicate.Client(api_token=API_TOKEN)
    # If its not a valid token, catch the exception
    except Exception as e:
        print(f"Error initializing Replicate client: {e}")
        client = None
# If the token is not found, client will remain None
else:
    print("[Warning] REPLICATE_API_TOKEN not found in credentials. Skipping image generation.")

def run_model(prompt):
    if client is None:
        print("Replicate client is not initialized. Cannot run model, skipping generation.")
        return None # Fall back not needed since already handled in views.py
    try:
        output = client.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "output_format": "png"
            }
        )
        return output
    except Exception as e:
        print(f"Error running model: {e}")
        return None