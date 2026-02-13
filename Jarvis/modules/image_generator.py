import replicate
import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


def generate_image(prompt):
    if not REPLICATE_API_TOKEN:
        return "Replicate API key missing."

    try:
        client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        output = client.run("stability-ai/sdxl", input={"prompt": prompt})
        image_url = output[0]
        webbrowser.open(image_url)
        return image_url
    except Exception as e:
        return f"Image generation error: {e}"
