import time
import schedule
import os
from utils.sleepUtils import get_sleep_data, fetch_sleep_data
from utils.quotes import get_affirmation_and_quote
from utils.quotes import morning_reminders
from utils.workouts import generate_daily_workout
from utils.oura import get_oura_readiness
import datetime
import random

def generate_combined_message():
    try:
        # Get sleep data
        sleep_data = fetch_sleep_data()
        
        # Create the combined message
        message = "🌞 YOUR DAILY MORNING UPDATE 🌞\n\n"
        
        # Add date and time
        current_time = datetime.datetime.now().strftime('%H:%M')
        day_name = datetime.datetime.now().strftime('%A')
        message += f"📅 {day_name}, {current_time}\n\n"
        
        # Add sleep data if available
        if sleep_data is not None:
            message += "🌙 SLEEP DATA:\n"
            if sleep_data['score']:
                message += f"⭐ Sleep Score: {sleep_data['score']:.1f}\n"
            
            if sleep_data['latency']:
                latency_minutes = int(sleep_data['latency'] // 60)
                message += f"⏱️ Time to Fall Asleep: {latency_minutes} minutes\n"
                
            if sleep_data['total_sleep_duration']:
                total_seconds = sleep_data['total_sleep_duration']
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                message += f"💤 Total Sleep: {hours}h {minutes}m\n"
                
                if total_seconds / 3600 >= 7.5:
                    message += "🎉 Great job getting enough sleep last night! Your body thanks you.\n"
                elif total_seconds / 3600 >= 6:
                    message += "👍 You got decent sleep, but your body could use a bit more rest.\n"
                else:
                    message += "❤️ You didn't get enough sleep last night. Be extra gentle with yourself today.\n"
            message += "\n"
        
        # Add morning reminders
        message += "📋 MORNING ROUTINE:\n"
        message += "• Prepare a full glass of water 💧\n"
        message += "• Mix your AG1 supplement 🥤\n"
        message += "• Prepare your BCAAs 💪\n"
        message += "• Pour your coffee ☕\n\n"
        
        message += "📅 DAILY PLANNING:\n"
        message += "• Review your calendar for today's meetings and commitments 📅\n"
        message += "• Update your to-do list with today's priorities ✅\n"
        message += "• Plan your day's schedule (work blocks, breaks, exercise) ⏱️\n"
        message += "• Set 1-3 main goals for the day 🎯\n\n"
        
        # Add workout data
        workout_message = generate_daily_workout()
        if workout_message:
            message += workout_message
            message += "\n\n"
        
        # Add affirmation and quote
        affirmation, quote = get_affirmation_and_quote()
        message += f"{affirmation}\n\n{quote}\n\n"
        
        # Add final motivational message
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
        print(f"Error generating combined message: {e}")
        print_notification("Could not generate daily update. Please try again later.")
        return None

# Schedule the combined message
# schedule.every().day.at("09:15").do(generate_combined_message)

# Test the function immediately
print("Testing combined message generator...")
generate_combined_message()

print("Message generator system running. Press CTRL+C to exit.")

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(50)