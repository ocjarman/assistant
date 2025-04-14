import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def print_notification(message):
    try:
        # Get the phone number from environment variables
        OLIVIA_PHONE_NUMBER = os.getenv('OLIVIA_PHONE')
        print("\n===== TERMINAL MESSAGE TEST =====")
        print(message)
        print("=====================\n")
    
        # Save to file
        with open("sleep_history.txt", "a") as file:
            file.write(f"\n[{datetime.datetime.now()}]\n{message}\n")
    
        # Send SMS using TextBelt
        # Truncate message if too long
        if len(message) > 1500:
            message = message[:1500] + "...\n(Message truncated)"
            
        # Send the SMS
        sanitized_message = sanitize_for_texting(message)
        # response = requests.post('https://textbelt.com/text', {
        #     'phone': OLIVIA_PHONE_NUMBER,
        #     'message': sanitized_message,
        #     'key': os.getenv('TEXTBELT_KEY'), 
        # })
        
        # result = response.json()
        # if result['success']:
        #     print(f"SMS sent successfully! Remaining: {result['quotaRemaining']}")
        # else:
        #     print(f"SMS failed: {result['error']}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


def sanitize_for_texting(message):
    """More aggressively modify message to avoid URL detection by TextBelt"""
    import re
    
    # Add spaces between numbers and punctuation that might look like URLs
    message = re.sub(r'(\d+)([.-])(\d+)', r'\1 \2 \3', message)
    
    # Add spaces in time formats
    message = re.sub(r'(\d+):(\d+)', r'\1 : \2', message)
    
    # Break up exercise set formats
    message = re.sub(r'(\d+)x(\d+)', r'\1 x \2', message)
    
    # Break up duration ranges 
    message = re.sub(r'(\d+)-(\d+)', r'\1 - \2', message)
    
    # Break up set/rep descriptions
    message = re.sub(r'sets of (\d+)', r'sets of  \1', message)
    message = re.sub(r'(\d+) reps', r'\1  reps', message)
    message = re.sub(r'(\d+) seconds', r'\1  seconds', message)
    
    # Add spaces around slashes (common in URL patterns)
    message = re.sub(r'(\w)/(\w)', r'\1 / \2', message)
    
    # Replace common URL-like terms with spaces between characters
    message = message.replace(".com", ". com")
    message = message.replace(".org", ". org")
    message = message.replace(".net", ". net")
    message = message.replace("http", "h t t p")
    message = message.replace("www.", "w w w .")
    
    return message

