from utils.print import print_notification
import json
import requests
import datetime
import random

def get_affirmation_and_quote():
    try:
        # Get a random quote
        quote_response = requests.get('https://zenquotes.io/api/random')
        quote_data = json.loads(quote_response.text)
        quote = f'✨ "{quote_data[0]["q"]}" - {quote_data[0]["a"]} ✨'

        # Get a random affirmation
        affirmation_response = requests.get('https://www.affirmations.dev/')
        affirmation_data = json.loads(affirmation_response.text)
        affirmation = f'💫 {affirmation_data["affirmation"]} 💫'
        
        return quote, affirmation
    except Exception as e:
        print(f"Error getting quote or affirmation: {e}")
        return "I am taking care of myself today, regardless of how much sleep I got.", "✨ The best preparation for tomorrow is doing your best today. ✨"

# morning reminders function based on recent sleep quality
def morning_reminders():
    try:
        current_time = datetime.datetime.now().strftime('%H:%M')
        day_name = datetime.datetime.now().strftime('%A')
        
        message = f"🌞 MORNING ROUTINE REMINDERS ({day_name}, {current_time})\n\n"
        
        # Desk preparation reminders
        message += "DESK PREPARATION:\n"
        message += "• Prepare a full glass of water 💧\n"
        message += "• Mix your AG1 supplement 🥤\n"
        message += "• Prepare your BCAAs 💪\n"
        message += "• Pour your coffee ☕\n\n"
        
        # Planning reminders
        message += "DAILY PLANNING:\n"
        message += "• Review your calendar for today's meetings and commitments 📅\n"
        message += "• Update your to-do list with today's priorities ✅\n"
        message += "• Plan your day's schedule (work blocks, breaks, exercise) ⏱️\n"
        message += "• Set 1-3 main goals for the day 🎯\n\n"
        
        # Add a motivational message for the day
        motivational_messages = [
            "Remember, how you start your morning sets the tone for your entire day!",
            "A well-prepared workspace leads to better focus and productivity.",
            "Taking a few minutes to plan now will save you hours later.",
            "Stay hydrated and nourished to keep your energy levels high all day.",
            "Setting clear intentions for the day helps you achieve what matters most."
        ]
        
        message += f"{random.choice(motivational_messages)} Have a great day! 🚀"
        
        print_notification(message)
        return message
    except Exception as e:
        print(f"Error generating morning reminders: {e}")
        print_notification("Could not generate morning reminders. Please try again later.")
