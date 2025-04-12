import time
import schedule
import os
from utils.sleepUtils import get_sleep_data
from utils.quotes import get_affirmation_and_quote
from utils.quotes import morning_reminders
from utils.workouts import generate_daily_workout
from utils.oura import get_oura_readiness_activity

# Schedule notifications
# Running at 7:00 AM to get the previous night's sleep data

# UNHIDE WHEN READY
schedule.every().day.at("07:00").do(get_sleep_data)  # Morning sleep report
schedule.every().day.at("08:00").do(morning_reminders)  # Daily workout at 8 AM
schedule.every().day.at("08:00").do(generate_daily_workout)  # Daily workout at 8 AM

# Test functions immediately
# print("Testing sleep printer and workout generator functions...")
#get_sleep_data()
#generate_daily_workout()
#morning_reminders()

print("Sleep-printer and workout generator system running. Press CTRL+C to exit.")

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(50)
