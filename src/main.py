import random
import time
import os
import json
from image_utils import read_trophies
from game_actions import drop_trophies, find_attack, drop_attack
from adb_utils import adb_tap
from image_utils import wait_for_template
from modes import get_user_input_with_timeout, force_drop_mode, force_loot_mode, normal_mode, legends_mode

def main():
    """Main function that prompts for mode selection and runs the appropriate mode."""
    print("=== Clash of Clans Auto-Farming Tool ===")

    # --- API Key Configuration ---
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        print("Please copy 'config.example.json' to 'config.json' and fill in the required values.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    api_key = config.get("gemini_api_key")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("Error: Gemini API key not configured.")
        print("Please edit 'config.json' and add your Gemini API key.")
        return

    os.environ['GEMINI_API_KEY'] = api_key
    print("Gemini API Key configured successfully.")
    # --- End of API Key Configuration ---

    print("Please select a mode:")
    print("1. Force_drop - Force trophy dropping")
    print("2. Force_loot - Force looting without trophy checks")
    print("3. Normal - Normal mode with trophy checks")
    print("4. Legends - Legends mode (currently same as normal)")
    
    mode_input = get_user_input_with_timeout("Enter mode (1-4 or mode name):", 20)
    
    # Process the input to determine the mode
    if mode_input:
        mode_input = mode_input.lower()
        if mode_input in ["1", "force_drop"]:
            print("Selected mode: Force Drop")
            force_drop_mode()
        elif mode_input in ["2", "force_loot"]:
            print("Selected mode: Force Loot")
            force_loot_mode()
        elif mode_input in ["3", "normal"]:
            print("Selected mode: Normal")
            normal_mode()
        elif mode_input in ["4", "legends"]:
            print("Selected mode: Legends")
            legends_mode()
        else:
            print("Invalid selection. Defaulting to Normal mode.")
            normal_mode()
    else:
        print("No selection made. Defaulting to Normal mode.")
        normal_mode()

if __name__ == "__main__":
    main()