import datetime
import requests 
import json
from dotenv import load_dotenv
import os
load_dotenv()


def get_oura_readiness_activity():
    """Retrieve readiness and activity scores from Oura Ring API"""
    try:
        oura_api_token = os.getenv('OURA_API_TOKEN')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        # Query for the last 2 days to ensure we have data
        two_days_ago = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        
        # Get readiness data
        readiness_url = "https://api.ouraring.com/v2/usercollection/daily_readiness"
        params = {"start_date": two_days_ago, "end_date": today}
        headers = {"Authorization": f"Bearer {oura_api_token}"}
        
        readiness_response = requests.get(readiness_url, headers=headers, params=params)
        readiness_data = json.loads(readiness_response.text)
        
        # Get activity data
        activity_url = "https://api.ouraring.com/v2/usercollection/daily_activity"
        activity_response = requests.get(activity_url, headers=headers, params=params)
        activity_data = json.loads(activity_response.text)
        
        # Default values if we can't get data
        readiness_score = 70  # Default to moderate readiness
        activity_score = 65   # Default to moderate activity
        
        # Extract scores from the response if available
        if 'data' in readiness_data and len(readiness_data['data']) > 0:
            # Get today's readiness data if available, otherwise get most recent
            today_readiness = next((item for item in readiness_data['data'] if item.get('day') == today), None)
            if today_readiness and 'score' in today_readiness:
                readiness_score = today_readiness['score']
            else:
                # If no data for today, get most recent
                readiness = sorted(readiness_data['data'], 
                                key=lambda x: x.get('day', ''), 
                                reverse=True)[0]
                if 'score' in readiness:
                    readiness_score = readiness['score']
        
        if 'data' in activity_data and len(activity_data['data']) > 0:
            # Get today's activity data if available, otherwise get most recent
            today_activity = next((item for item in activity_data['data'] if item.get('day') == today), None)
            if today_activity and 'score' in today_activity:
                activity_score = today_activity['score']
            else:
                # If no data for today, get most recent
                activity = sorted(activity_data['data'], 
                                key=lambda x: x.get('day', ''), 
                                reverse=True)[0]
                if 'score' in activity:
                    activity_score = activity['score']
        
        return readiness_score, activity_score
    
    except Exception as e:
        print(f"Error getting Oura data: {e}")
        # Return default moderate values if we can't get actual data
        return 70, 65