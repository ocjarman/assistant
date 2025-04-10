import datetime
import time
import requests
import json
from utils.print import print_notification, sanitize_for_texting
from utils.quotes import get_affirmation_and_quote

def get_sleep_data():
    try:
        oura_api_token = "3HQMWLUXSEHCZYEDARFGLIIMX3U5DCPM"
        
        # Get today's date and yesterday's date to ensure we capture the most recent night's sleep
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Use the sleep sessions endpoint with yesterday and today to get the most recent sleep
        url = "https://api.ouraring.com/v2/usercollection/sleep"
        params = {"start_date": yesterday, "end_date": today}
        
        headers = {"Authorization": f"Bearer {oura_api_token}"}
        
        response = requests.get(url, headers=headers, params=params)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"ERROR: API returned status code {response.status_code}")
            print_notification(f"Error fetching sleep data. Status code: {response.status_code}")
            return
        
        data = json.loads(response.text)
        
        # Check if we have data
        if 'data' not in data or len(data['data']) == 0:
            print("No sleep data found in response")
            print_notification("No sleep data available.")
            return
        
        # If we have multiple sleep sessions, sort them by bedtime_start to get the most recent one
        if len(data['data']) > 1:
            sorted_sessions = sorted(data['data'], 
                                    key=lambda x: x.get('bedtime_start', ''), 
                                    reverse=True)
            session = sorted_sessions[0]
        else:
            session = data['data'][0]
        
        message = f"🌙 Olivia's Personalized Daily Motivation 🌙\n"
        
        # Add sleep date
        if 'day' in session:
            message += f"📅 Date: {session['day']}\n\n"
        
        # Function to format seconds to hours and minutes
        def format_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        
        # Add sleep score if available
        if 'score' in session:
            message += f"⭐ Sleep Score: {session['score']}\n"
        
        # Add sleep latency (time to fall asleep)
        if 'latency' in session:
            # Latency is typically in seconds
            latency_minutes = int(session['latency'] // 60)
            message += f"⏱️ Time to Fall Asleep: {latency_minutes} minutes\n"
            
        # Get total sleep duration
        if 'total_sleep_duration' in session:
            total_seconds = session['total_sleep_duration']
            total_hours = total_seconds / 3600  # Convert seconds to hours
            total_sleep = format_time(total_seconds)
            message += f"💤 Total Sleep: {total_sleep}\n\n"
            
            # Create a personalized message based on sleep duration
            if total_hours >= 7.5:
                prefix = "🎉 Great job getting enough sleep last night! Your body thanks you."
            elif total_hours >= 6:
                prefix = "👍 You got decent sleep, but your body could use a bit more rest."
            else:
                prefix = "❤️ You didn't get enough sleep last night. Be extra gentle with yourself today."
            
            message += f"{prefix}\n\n"
            
            # Add affirmation and quote
            affirmation, quote = get_affirmation_and_quote()
            message += f"{affirmation}\n\n{quote}"
            
        print_notification(message)
    except Exception as e:
        print(f"Error getting sleep data: {e}")
        print_notification(f"Could not retrieve sleep data. Error: {e}")