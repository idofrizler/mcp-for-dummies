from io import BytesIO
import requests
from PIL import Image
from mcp.server.fastmcp import FastMCP
from typing import Tuple, Dict, List
from collections import Counter


mcp = FastMCP("Detect Colors 101")


def is_within_range(value: int, min_val: int, max_val: int) -> bool:
    """Check if a value falls within the specified range (inclusive)."""
    return min_val <= value <= max_val


def channels_are_similar(r: int, g: int, b: int, threshold: int = 30) -> bool:
    """Check if RGB channels are within a threshold of each other."""
    return (abs(r - g) < threshold and 
            abs(g - b) < threshold and 
            abs(r - b) < threshold)


def classify_pixel(r: int, g: int, b: int) -> str:
    """
    Classify a single pixel into a color category based on its RGB values.
    """
    # Achromatic colors
    if is_within_range(r, 200, 255) and is_within_range(g, 200, 255) and is_within_range(b, 200, 255):
        return "white"
    
    if is_within_range(r, 0, 50) and is_within_range(g, 0, 50) and is_within_range(b, 0, 50):
        return "black"
    
    if channels_are_similar(r, g, b):
        if r > 150:  # Light grey
            return "white"
        elif r < 50:  # Dark grey
            return "black"
        return "grey"

    # Calculate color intensities
    max_channel = max(r, g, b)
    min_channel = min(r, g, b)
    diff = max_channel - min_channel
    
    # If the difference between channels is too small, it's a shade of grey
    if diff < 30:
        return "grey"

    # Determine the dominant channel and classify accordingly
    if r > g and r > b:  # Red is dominant
        if g > 150:  # High green component
            if b < 100 and abs(r - g) < 50:  # Similar red and green, low blue
                return "yellow"
            elif b > 150:  # High blue
                return "pink"
            else:
                return "orange"
        elif g < 100 and b < 100:  # Low values in other channels
            return "red"
        elif b > 150:  # High blue
            return "purple"
        return "red"
    
    elif g > r and g > b:  # Green is dominant
        if r > 180 and b < 100:  # High red, low blue
            return "yellow"
        elif r < 100 and b < 100:  # Low values in other channels
            return "green"
        return "green"
    
    else:  # Blue is dominant
        if r > 150 and g < 150:  # High red, low green
            return "purple"
        elif r < 150 and g < 150:  # Low values in other channels
            return "blue"
        return "blue"


def get_color_distribution(image: Image) -> Dict[str, int]:
    """
    Analyze the image and return the distribution of colors.
    """
    # Convert image to RGB mode if it isn't already
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    color_counts = Counter()

    # Process each pixel
    for x in range(width):
        for y in range(height):
            r, g, b = rgb_image.getpixel((x, y))
            color = classify_pixel(r, g, b)
            color_counts[color] += 1

    return dict(color_counts)


@mcp.tool(description="Analyzes an image from a URL and determines its dominant color, grouping similar shades into basic color categories.")
def get_dominant_color(image_url: str) -> str:
    """
    Analyzes the image at the given URL and returns the dominant color.
    Colors are classified by analyzing each pixel and grouping similar shades together.

    Args:
        image_url (str): URL of the image to analyze

    Returns:
        str: The most common color category in the image

    Raises:
        Exception: If there's an error fetching or processing the image
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except Exception as e:
        return f"Error fetching image: {e}"

    try:
        image = Image.open(BytesIO(response.content))
        # Resize to reduce processing time while maintaining aspect ratio
        image.thumbnail((100, 100))
        
        # Get the distribution of colors
        color_distribution = get_color_distribution(image)
        
        if not color_distribution:
            return "Unknown"
        
        # Return the most common color
        return max(color_distribution.items(), key=lambda x: x[1])[0]
        
    except Exception as e:
        return f"Error processing image: {e}"


if __name__ == "__main__":
    """Run the MCP server."""
    print("Starting MCP server...")
    mcp.run()
