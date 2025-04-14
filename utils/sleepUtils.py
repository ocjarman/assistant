import datetime
import time
import requests
import json
from utils.print import print_notification, sanitize_for_texting
from utils.quotes import get_affirmation_and_quote

def fetch_sleep_data():
    """Fetch sleep data from Oura API without printing any messages"""
    try:
        oura_api_token = "3HQMWLUXSEHCZYEDARFGLIIMX3U5DCPM"
        
        # Get today's date and calculate the date range for last night's sleep
        today = datetime.datetime.now().date()
        start_date = today.strftime('%Y-%m-%d')
        end_date = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        
        # First, get the detailed sleep session data
        sleep_url = "https://api.ouraring.com/v2/usercollection/sleep"
        params = {"start_date": start_date, "end_date": end_date}
        headers = {"Authorization": f"Bearer {oura_api_token}"}
        
        sleep_response = requests.get(sleep_url, headers=headers, params=params)
        
        # Check if the request was successful
        if sleep_response.status_code != 200:
            print(f"ERROR: Sleep API returned status code {sleep_response.status_code}")
            return None
        
        sleep_data = json.loads(sleep_response.text)
        
        # Check if we have sleep session data
        if 'data' not in sleep_data or len(sleep_data['data']) == 0:
            print("No sleep session data found in response")
            return None
        
        # Get the most recent sleep session
        if len(sleep_data['data']) > 1:
            sorted_sessions = sorted(sleep_data['data'], 
                                    key=lambda x: x.get('bedtime_start', ''), 
                                    reverse=True)
            session = sorted_sessions[0]
        else:
            session = sleep_data['data'][0]
        
        # Now, get the overall sleep score from the daily_sleep endpoint
        daily_sleep_url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
        daily_sleep_response = requests.get(daily_sleep_url, headers=headers, params=params)
        
        if daily_sleep_response.status_code != 200:
            print(f"ERROR: Daily Sleep API returned status code {daily_sleep_response.status_code}")
            # Continue with sleep session data even if daily sleep score fails
            sleep_score = 0
        else:
            daily_sleep_data = json.loads(daily_sleep_response.text)
            if 'data' in daily_sleep_data and len(daily_sleep_data['data']) > 0:
                sleep_score = daily_sleep_data['data'][0].get('score', 0)
            else:
                sleep_score = 0
        
        # Create a dictionary with the sleep data we need
        return {
            'total_sleep_duration': session.get('total_sleep_duration', 0),
            'score': sleep_score,
            'latency': session.get('latency', 0)
        }
        
    except Exception as e:
        print(f"Error getting sleep data: {e}")
        return None

def get_sleep_data():
    """Get sleep data and print a notification message"""
    try:
        sleep_data = fetch_sleep_data()
        
        if sleep_data is None:
            print_notification("Could not retrieve sleep data.")
            return None
        
        # Create and print the notification message
        message = f"🌙 Olivia's Personalized Daily Motivation 🌙\n"
        message += f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        if sleep_data['score']:
            message += f"⭐ Sleep Score: {sleep_data['score']:.1f}\n"
        
        if sleep_data['latency']:
            latency_minutes = int(sleep_data['latency'] // 60)
            message += f"⏱️ Time to Fall Asleep: {latency_minutes} minutes\n"
            
        if sleep_data['total_sleep_duration']:
            total_seconds = sleep_data['total_sleep_duration']
            total_hours = total_seconds / 3600
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            message += f"💤 Total Sleep: {hours}h {minutes}m\n\n"
            
            if total_hours >= 7.5:
                prefix = "🎉 Great job getting enough sleep last night! Your body thanks you."
            elif total_hours >= 6:
                prefix = "👍 You got decent sleep, but your body could use a bit more rest."
            else:
                prefix = "❤️ You didn't get enough sleep last night. Be extra gentle with yourself today."
            
            message += f"{prefix}\n\n"
            
            affirmation, quote = get_affirmation_and_quote()
            message += f"{affirmation}\n\n{quote}"
        
        print_notification(message)
        return sleep_data
        
    except Exception as e:
        print(f"Error in get_sleep_data: {e}")
        print_notification(f"Could not process sleep data. Error: {e}")
        return None