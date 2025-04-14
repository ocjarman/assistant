import datetime
import requests 
import json
from dotenv import load_dotenv
import os
load_dotenv()


def get_oura_readiness():
    """Retrieve readiness score from Oura Ring API"""
    try:
        oura_api_token = os.getenv('OURA_API_TOKEN')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Get readiness data
        readiness_url = "https://api.ouraring.com/v2/usercollection/daily_readiness"
        params = {"start_date": today, "end_date": today}
        headers = {"Authorization": f"Bearer {oura_api_token}"}
        
        readiness_response = requests.get(readiness_url, headers=headers, params=params)
        if readiness_response.status_code != 200:
            print(f"Error: Readiness API returned status code {readiness_response.status_code}")
            return 70
            
        readiness_data = json.loads(readiness_response.text)
        
        # Default value if we can't get data
        readiness_score = 70  # Default to moderate readiness
        
        # Extract score from the response if available
        if 'data' in readiness_data and len(readiness_data['data']) > 0:
            # Get the first (and should be only) readiness entry for today
            readiness_entry = readiness_data['data'][0]
            if 'score' in readiness_entry:
                readiness_score = readiness_entry['score']
        else:
            print("No readiness data available for today")
        # Debug print
        return readiness_score
    
    except Exception as e:
        print(f"Error getting Oura data: {e}")
        # Return default moderate value if we can't get actual data
        return 70