import replicate
import cred

client = replicate.Client(api_token=cred.REPLICATE_API_TOKEN)

def run_model():
    output = client.run(
        "black-forest-labs/flux-schnell",
        input={"prompt": "an iguana on the beach, pointillism"}
    )
    return output