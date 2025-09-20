import os
import json
import google.generativeai as genai
from PIL import Image

def get_deployment_coords_from_gemini(image_path, town_hall_location):
    """
    Analyzes the game screenshot with Gemini to determine strategic troop deployment points.

    Args:
        image_path (str): The path to the screenshot of the game.
        town_hall_location (tuple): A tuple (x, y) of the Town Hall's coordinates.

    Returns:
        list: A list of dictionaries, where each dictionary is a coordinate point, e.g.,
              [{"x": 100, "y": 200}, {"x": 150, "y": 250}].
              Returns None if the API call fails or the response is invalid.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not found.")
        return None

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-pro-vision')

        image = Image.open(image_path)

        prompt = f"""
        You are an expert Clash of Clans strategist. Analyze this screenshot of an enemy base.
        The screen resolution is 2400x1080.
        The enemy Town Hall is located at approximately {town_hall_location}.

        Your task is to identify 4 optimal points to deploy troops along the outer red line of the play area.
        The goal is to attack the base effectively, starting with a line of troops.
        The points should form a strategic line or arc on one side of the base.

        Return your answer as a JSON object with a single key "deploy_points", which is a list of 4 coordinate objects.
        Do not provide any explanation or introductory text, only the JSON object.
        Example format:
        {{
            "deploy_points": [
                {{"x": 800, "y": 250}},
                {{"x": 900, "y": 300}},
                {{"x": 1000, "y": 350}},
                {{"x": 1100, "y": 400}}
            ]
        }}
        """

        print("Sending request to Gemini AI...")
        response = model.generate_content([prompt, image])

        # Clean up the response to extract only the JSON part.
        response_text = response.text.strip().replace('```json', '').replace('```', '').strip()

        print("Received response from Gemini AI.")

        # Parse the JSON response
        data = json.loads(response_text)

        # Validate the response structure
        if "deploy_points" in data and isinstance(data["deploy_points"], list):
            # Further validation can be added here to check x, y keys
            print(f"Successfully parsed deployment points: {data['deploy_points']}")
            return data["deploy_points"]
        else:
            print("Error: Invalid JSON structure in Gemini response.")
            return None

    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        return None
