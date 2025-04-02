import os
import requests
from mcp import tool  # Assumes that the mcp module is available

@tool
def analyze_image(image_url: str) -> str:
    """
    Connects to an online image analysis service using an API key from the environment variables.
    Returns the analysis result as a string.
    """
    api_key = os.environ.get("IMAGE_API_KEY")
    if not api_key:
        return "Error: IMAGE_API_KEY is not set."
    try:
        # Properly encode the image URL
        encoded_url = requests.utils.quote(image_url, safe='')
        response = requests.get(f"https://api.example.com/analyze?img={encoded_url}&apikey={api_key}")
        response.raise_for_status()
        data = response.json()
        return str(data)
    except Exception as e:
        return f"Error during image analysis: {e}"

if __name__ == "__main__":
    # Example usage
    image_url = "https://example.com/sample.jpg"
    result = analyze_image(image_url)
    print("Analysis Result:", result)
