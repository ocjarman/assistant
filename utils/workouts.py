import datetime
import random

from .print import print_notification
from utils.oura import get_oura_readiness
from utils.sleepUtils import fetch_sleep_data

def generate_cardio_workout(day_of_week, intensity="moderate"):
    """Generate a cardio component for the daily workout based on intensity level"""
    import random
    import math
    
    # Different cardio types based on days of the week and intensity
    cardio_options = {
        "high": {
            0: ["Tempo Run", "Fartlek Training", "Peloton HIIT Ride"],  # Monday
            1: ["Interval Run", "Hill Repeats", "Peloton Tabata Ride"],  # Tuesday
            2: ["Speed Intervals", "Tempo Run", "Peloton Power Zone Max Ride"],  # Wednesday
            3: ["Fartlek Training", "Pyramid Intervals", "Peloton HIIT & Hills Ride"],  # Thursday
            4: ["Tempo Run", "Speed Play", "Peloton Climb Ride"],  # Friday
            5: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"],  # Saturday
            6: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"]   # Sunday
        },
        "moderate": {
            0: ["Tempo Run", "Fartlek Training", "Peloton Power Zone Ride"],  # Monday
            1: ["Steady State Jog", "Light Recovery Run", "Peloton Interval Ride"],  # Tuesday
            2: ["Hill Repeats", "Speed Intervals", "Peloton HIIT Ride"],  # Wednesday
            3: ["Easy Run", "Steady State Cardio", "Peloton Music Ride"],  # Thursday
            4: ["Tempo Run", "Aerobic Base Building", "Peloton Groove Ride"],  # Friday
            5: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"],  # Saturday
            6: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"]   # Sunday
        },
        "low": {
            0: ["Easy Jog", "Light Cardio", "Peloton Low Impact Ride"],  # Monday
            1: ["Steady State Walk/Jog", "Recovery Jog", "Peloton Recovery Ride"],  # Tuesday
            2: ["Easy Intervals", "Light Hill Work", "Peloton Beginner Ride"],  # Wednesday
            3: ["Recovery Run", "Easy Cardio", "Peloton Low Impact Ride"],  # Thursday
            4: ["Light Fartlek", "Easy Tempo", "Peloton Scenic Ride"],  # Friday
            5: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"],  # Saturday
            6: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"]   # Sunday
        },
        "recovery": {
            0: ["Walking", "Light Mobility", "Peloton Recovery Ride"],  # Monday
            1: ["Recovery Walk", "Gentle Movement", "Peloton Cool Down Ride"],  # Tuesday
            2: ["Easy Walking", "Mobility Circuits", "Peloton Beginner Ride"],  # Wednesday
            3: ["Gentle Movement", "Recovery Walk", "Peloton Low Impact Ride"],  # Thursday
            4: ["Walking", "Mobility Flow", "Peloton Recovery Ride"],  # Friday
            5: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"],  # Saturday
            6: ["Long Run (4-6 miles)", "Long Run (4-6 miles)", "Long Run (4-6 miles)"]   # Sunday
        }
    }
    
    # Get cardio options based on intensity level
    intensity_options = cardio_options.get(intensity, cardio_options["moderate"])
    
    # Randomly select a cardio type for today based on the day of the week
    cardio_type = random.choice(intensity_options[day_of_week])
    
    # Generate duration based on intensity
    # Determine if this is a Peloton workout
    is_peloton = "Peloton" in cardio_type
    
    if intensity == "high":
        duration = random.randint(30, 45) if is_peloton else random.randint(25, 30)
    elif intensity == "moderate":
        duration = random.randint(20, 30) if is_peloton else random.randint(20, 25)
    elif intensity == "low":
        duration = random.randint(20, 30) if is_peloton else random.randint(15, 20)
    else:  # recovery
        duration = random.randint(20, 30) if is_peloton else random.randint(10, 15)
    
    # Generate specific instructions based on the cardio type and intensity
    if "Long Run" in cardio_type:
        # For weekends, always do a long run with stretching
        # Randomly choose between distance-based or time-based run
        if random.random() < 0.5:
            # Distance-based run
            miles = random.uniform(4.0, 6.0)
            return f"{cardio_type}\n• 5-10 min warmup at easy pace\n• {miles:.1f} miles at a comfortable, conversational pace\n• 5-10 min cooldown\n• 10-15 minutes of post-run stretching focusing on:\n  - Hamstrings\n  - Quadriceps\n  - Hip flexors\n  - Calves\n  - Lower back"
        else:
            # Time-based run
            duration = random.randint(45, 60)
            return f"{cardio_type}\n• 5-10 min warmup at easy pace\n• {duration} minutes at a comfortable, conversational pace\n• 5-10 min cooldown\n• 10-15 minutes of post-run stretching focusing on:\n  - Hamstrings\n  - Quadriceps\n  - Hip flexors\n  - Calves\n  - Lower back"
    elif "Peloton" in cardio_type:
        # Round to nearest 5 for Peloton durations (classes are 20, 30, 45 min)
        peloton_duration = round(duration / 5) * 5
        # Ensure duration is between 20 and 45 minutes
        if peloton_duration < 20:
            peloton_duration = 20
        elif peloton_duration > 45:
            peloton_duration = 45
        
        # Determine class type description based on intensity
        if intensity == "high":
            description = f"challenging {peloton_duration} minute class that will push your limits"
        elif intensity == "moderate":
            description = f"moderate {peloton_duration} minute class to build endurance and strength"
        elif intensity == "low":
            description = f"lighter {peloton_duration} minute class focusing on form and technique"
        else:  # recovery
            description = f"gentle {peloton_duration} minute class to promote active recovery"
            
        return f"{cardio_type}: {peloton_duration} minutes\n• A {description}"
    elif "Tempo" in cardio_type and intensity != "recovery":
        return f"{cardio_type}: {duration} minutes\n• 5 min warmup at easy pace\n• {duration-10} min at {'challenging' if intensity == 'high' else 'moderate'} but sustainable pace\n• 5 min cooldown at easy pace"
    elif ("Interval" in cardio_type or "Repeats" in cardio_type) and intensity != "recovery":
        # Adjust intervals based on intensity
        if intensity == "high":
            interval_time = random.choice([45, 60, 75])
            rest_time = random.choice([30, 45])
        elif intensity == "moderate":
            interval_time = random.choice([30, 45, 60])
            rest_time = random.choice([30, 45, 60])
        else:  # low
            interval_time = random.choice([20, 30, 45])
            rest_time = random.choice([45, 60, 75])
            
        sets = math.ceil((duration * 60 * 0.7) / (interval_time + rest_time))
        effort_level = "hard" if intensity == "high" else "moderate" if intensity == "moderate" else "light"
        return f"{cardio_type}: ~{duration} minutes\n• 5 min warmup\n• {sets} sets of {interval_time}s {effort_level} effort + {rest_time}s recovery\n• 5 min cooldown"
    elif "Fartlek" in cardio_type and intensity != "recovery":
        return f"{cardio_type}: {duration} minutes\n• 5 min warmup\n• {duration-10} min of alternating between {'high' if intensity == 'high' else 'moderate' if intensity == 'moderate' else 'light'} and low intensity at random intervals\n• 5 min cooldown"
    elif "Walk" in cardio_type or intensity == "recovery":
        return f"{cardio_type}: {duration} minutes at a gentle, comfortable pace focusing on recovery"
    else:
        return f"{cardio_type}: {duration} minutes at a {'brisk' if intensity == 'high' else 'comfortable, conversational' if intensity == 'moderate' else 'relaxed'} pace"

def generate_daily_workout():
    try:
        # Get day of week (0 = Monday, 6 = Sunday)
        day_of_week = datetime.datetime.now().weekday()
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day_of_week]
        
        # Get readiness score from Oura Ring
        readiness_score = get_oura_readiness()
        
        # Get sleep data
        sleep_data = fetch_sleep_data()
        
        # Initialize sleep metrics with default values
        total_sleep = 0
        sleep_score = 0
        sleep_latency = 0
        sleep_messages = []
        
        if sleep_data is not None:
            total_sleep = sleep_data.get('total_sleep_duration', 0) / 3600  # Convert to hours
            sleep_score = sleep_data.get('score', 0)
            sleep_latency = sleep_data.get('latency', 0) / 60  # Convert to minutes
            
            # Adjust for sleep duration
            if total_sleep < 6:
                sleep_messages.append("Sleep duration was below 6 hours, so we're taking it easier today.")
            elif total_sleep >= 7.5:
                sleep_messages.append("Great sleep duration! We can push a bit harder today.")
            
            # Adjust for sleep quality
            if sleep_score < 70:
                sleep_messages.append("Sleep quality was below optimal, so we're being more conservative.")
            elif sleep_score >= 85:
                sleep_messages.append("Excellent sleep quality! We can challenge ourselves more.")
            
            # Adjust for sleep latency
            if sleep_latency > 30:
                sleep_messages.append("It took longer to fall asleep, so we're being more gentle.")
        else:
            sleep_messages.append("No sleep data available. Using readiness score only for workout intensity.")
        
        # Determine base intensity based on readiness score
        if readiness_score >= 85:
            base_intensity = "high"
        elif readiness_score >= 70:
            base_intensity = "moderate"
        elif readiness_score >= 50:
            base_intensity = "low"
        else:
            base_intensity = "recovery"
        
        # Adjust intensity based on sleep metrics
        final_intensity = base_intensity
        
        # Apply sleep-based adjustments if we have sleep data
        if sleep_data is not None:
            if total_sleep < 6 and final_intensity != "recovery":
                final_intensity = downgrade_intensity(final_intensity)
            elif total_sleep >= 7.5 and final_intensity != "high":
                final_intensity = upgrade_intensity(final_intensity)
            
            if sleep_score < 70 and final_intensity != "recovery":
                final_intensity = downgrade_intensity(final_intensity)
            elif sleep_score >= 85 and final_intensity != "high":
                final_intensity = upgrade_intensity(final_intensity)
            
            if sleep_latency > 30 and final_intensity != "recovery":
                final_intensity = downgrade_intensity(final_intensity)
        
        # Create intensity description
        intensity_description = f"Your readiness score is {readiness_score}.\n"
        for message in sleep_messages:
            intensity_description += f"{message}\n"
        intensity_description += "\n"
        
        # Generate today's workout based on the day of week and intensity
        cardio_component = generate_cardio_workout(day_of_week, final_intensity)
        strength_component = generate_strength_workout(day_of_week, final_intensity)
        
        message = f"💪 YOUR DAILY WORKOUT FOR {day_name.upper()}\n\n"
        message += f"🧘‍♀️OURA DATA: Readiness {readiness_score}\n"
        if sleep_data is not None:
            message += f"🌙 SLEEP DATA: {total_sleep:.1f}h | Score {sleep_score:.1f} | Latency {sleep_latency:.0f}min \n\n"
        message += f"{intensity_description}\n"
        message += f"FOCUS TODAY: {strength_component['focus']}\n\n"
        message += "🏃‍♀️CARDIO PORTION\n"
        message += f"{cardio_component.replace('-', ' to ').replace(':', ' ')}\n\n"
        message += "🏋️‍♀️ STRENGTH PORTION\n"
        message += strength_component['workout'].replace('-', ' to ').replace(':', ' ')
        
        # Add a motivational closer
        motivational_closers = [
            "🏆 You got this",
            "⚡ Embrace the challenge today",
            "🎯 Showing up is half the battle",
            "🧘‍♀️ Your future self thanks you",
            "💪 Progress over perfection"
        ]
        
        message += f"\n\n{random.choice(motivational_closers)}"
        return message
    except Exception as e:
        print(f"Error generating workout: {e}")
        print_notification("Could not generate today's workout. Please try again later.")
        return None

def downgrade_intensity(current_intensity):
    """Downgrade workout intensity by one level"""
    intensity_levels = ["high", "moderate", "low", "recovery"]
    current_index = intensity_levels.index(current_intensity)
    
    # If already at recovery, keep it there
    if current_index >= len(intensity_levels) - 1:
        return intensity_levels[-1]
    
    # Otherwise downgrade one level
    return intensity_levels[current_index + 1]

def upgrade_intensity(current_intensity):
    """Upgrade workout intensity by one level"""
    intensity_levels = ["recovery", "low", "moderate", "high"]
    current_index = intensity_levels.index(current_intensity)
    
    # If already at high, keep it there
    if current_index >= len(intensity_levels) - 1:
        return intensity_levels[-1]
    
    # Otherwise upgrade one level
    return intensity_levels[current_index + 1]

def generate_strength_workout(day_of_week, intensity="moderate"):
    """Generate a strength/HIIT workout component based on the day of the week and intensity level"""
    import math
    
    # Define muscle group focus for each day
    focus_by_day = {
        0: "Upper Body - Push",       # Monday
        1: "Lower Body",              # Tuesday
        2: "Upper Body - Pull",       # Wednesday
        3: "Full Body",               # Thursday
        4: "Core & Mobility",         # Friday
        5: "Total Body HIIT",         # Saturday
        6: "Active Recovery & Core"   # Sunday
    }
    
    # Override focus if in recovery mode
    if intensity == "recovery":
        focus_by_day = {day: "Recovery & Mobility" for day in range(7)}
    
    # Randomly decide between strength training and Pilates (30% chance for Pilates)
    if random.random() < 0.3:
        pilates_duration = random.choice([10, 15, 20])
        return {
            "focus": "Pilates",
            "workout": f"PILATES SESSION ({pilates_duration} minutes):\n• Focus on core engagement and controlled movements\n• Include exercises for:\n  - Core strength\n  - Hip stability\n  - Spinal mobility\n  - Postural alignment\n• End with 5 minutes of deep breathing and relaxation"
        }
    
    # Exercise database by muscle group
    # Each entry includes: [name, equipment, format (reps or time), details by intensity]
    exercise_db = {
        "upper_push": [
            ["Push-ups", "bodyweight", "reps", {
                "high": "4 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "1 set of 5-8 reps (focus on form)"
            }],
            ["Dumbbell Bench Press", "dumbbell", "reps", {
                "high": "4 sets of 10-12 reps (heavier weight)", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2-3 sets of 8-10 reps (lighter weight)", 
                "recovery": "Avoid today"
            }],
            ["Shoulder Press", "dumbbell", "reps", {
                "high": "4 sets of 10-12 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps (lighter weight)", 
                "recovery": "Avoid today"
            }],
            ["Tricep Dips", "bodyweight", "reps", {
                "high": "3 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "Gentle arm extensions - 1 set of 10"
            }],
            ["Incline Push-ups", "bodyweight", "reps", {
                "high": "3 sets of 15-20 reps", 
                "moderate": "3 sets of 12-15 reps", 
                "low": "2 sets of 10-12 reps", 
                "recovery": "1 set of 8-10 reps (use higher incline)"
            }],
            ["Tricep Extensions", "dumbbell", "reps", {
                "high": "3 sets of 15 reps", 
                "moderate": "3 sets of 12-15 reps", 
                "low": "2 sets of 10-12 reps", 
                "recovery": "Avoid today"
            }]
        ],
        "upper_pull": [
            ["Dumbbell Rows", "dumbbell", "reps", {
                "high": "4 sets of 12 reps each side", 
                "moderate": "3 sets of 10-12 reps each side", 
                "low": "2 sets of 8-10 reps each side", 
                "recovery": "Avoid today"
            }],
            ["Superman Hold", "bodyweight", "time", {
                "high": "3 sets of 45-60 seconds", 
                "moderate": "3 sets of 30-45 seconds", 
                "low": "2 sets of 20-30 seconds", 
                "recovery": "1 set of 15-20 seconds"
            }],
            ["Bicep Curls", "dumbbell", "reps", {
                "high": "4 sets of 12 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "Avoid today"
            }],
            ["Reverse Snow Angels", "bodyweight", "reps", {
                "high": "3 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "1 set of 8 reps (focus on form)"
            }],
            ["Bent-Over Lateral Raises", "dumbbell", "reps", {
                "high": "3 sets of 15 reps", 
                "moderate": "3 sets of 12-15 reps", 
                "low": "2 sets of 10-12 reps", 
                "recovery": "Avoid today"
            }],
            ["Hammer Curls", "dumbbell", "reps", {
                "high": "3 sets of 15 reps", 
                "moderate": "3 sets of 12 reps", 
                "low": "2 sets of 10 reps", 
                "recovery": "Avoid today"
            }]
        ],
        "lower_body": [
            ["Squats", "bodyweight", "reps", {
                "high": "4 sets of 15-20 reps", 
                "moderate": "3 sets of 12-15 reps", 
                "low": "2-3 sets of 10-12 reps", 
                "recovery": "1 set of 8 reps (partial range of motion)"
            }],
            ["Lunges", "bodyweight", "reps", {
                "high": "4 sets of 12 reps each leg", 
                "moderate": "3 sets of 10 reps each leg", 
                "low": "2 sets of 8 reps each leg", 
                "recovery": "1 set of 5 reps each leg (supported)"
            }],
            ["Glute Bridges", "bodyweight", "reps", {
                "high": "3 sets of 15-20 reps", 
                "moderate": "3 sets of 12-15 reps", 
                "low": "2 sets of 10-12 reps", 
                "recovery": "2 sets of 8-10 reps"
            }],
            ["Calf Raises", "bodyweight", "reps", {
                "high": "3 sets of 20 reps", 
                "moderate": "3 sets of 15 reps", 
                "low": "2 sets of 12 reps", 
                "recovery": "1 set of 10 reps"
            }],
            ["Goblet Squats", "dumbbell", "reps", {
                "high": "4 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "Avoid today"
            }],
            ["Romanian Deadlifts", "dumbbell", "reps", {
                "high": "4 sets of 12 reps", 
                "moderate": "3 sets of 10 reps", 
                "low": "2 sets of 8 reps", 
                "recovery": "Avoid today"
            }]
        ],
        "core": [
            ["Plank", "bodyweight", "time", {
                "high": "3 sets of 45-60 seconds", 
                "moderate": "3 sets of 30-45 seconds", 
                "low": "2 sets of 20-30 seconds", 
                "recovery": "1 set of 15-20 seconds"
            }],
            ["Russian Twists", "bodyweight", "reps", {
                "high": "3 sets of 20 reps (10 each side)", 
                "moderate": "3 sets of 16 reps (8 each side)", 
                "low": "2 sets of 12 reps (6 each side)", 
                "recovery": "1 set of 6 reps total (3 each side)"
            }],
            ["Dead Bugs", "bodyweight", "reps", {
                "high": "3 sets of 12 reps each side", 
                "moderate": "3 sets of 10 reps each side", 
                "low": "2 sets of 8 reps each side", 
                "recovery": "1 set of 5 reps each side"
            }],
            ["Bicycle Crunches", "bodyweight", "reps", {
                "high": "3 sets of 30 reps (15 each side)", 
                "moderate": "3 sets of 24 reps (12 each side)", 
                "low": "2 sets of 16 reps (8 each side)", 
                "recovery": "1 set of 10 reps total"
            }],
            ["Mountain Climbers", "bodyweight", "time", {
                "high": "3 sets of 45 seconds", 
                "moderate": "3 sets of 30 seconds", 
                "low": "2 sets of 20 seconds", 
                "recovery": "Avoid today"
            }]
        ],
        "full_body": [
            ["Burpees", "bodyweight", "reps", {
                "high": "3 sets of 15 reps", 
                "moderate": "3 sets of 10 reps", 
                "low": "2 sets of 8 reps", 
                "recovery": "Avoid today"
            }],
            ["Dumbbell Thrusters", "dumbbell", "reps", {
                "high": "3 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "Avoid today"
            }],
            ["Mountain Climbers", "bodyweight", "time", {
                "high": "3 sets of 45 seconds", 
                "moderate": "3 sets of 30 seconds", 
                "low": "2 sets of 20 seconds", 
                "recovery": "Avoid today"
            }],
            ["Renegade Rows", "dumbbell", "reps", {
                "high": "3 sets of 12 reps each side", 
                "moderate": "3 sets of 10 reps each side", 
                "low": "2 sets of 8 reps each side", 
                "recovery": "Avoid today"
            }],
            ["Squat to Press", "dumbbell", "reps", {
                "high": "3 sets of 12-15 reps", 
                "moderate": "3 sets of 10-12 reps", 
                "low": "2 sets of 8-10 reps", 
                "recovery": "Avoid today"
            }]
        ],
        "hiit": [
            ["Jumping Jacks", "bodyweight", "time", {
                "high": "45 seconds work, 15 seconds rest", 
                "moderate": "30 seconds work, 20 seconds rest", 
                "low": "20 seconds work, 20 seconds rest", 
                "recovery": "Avoid today"
            }],
            ["High Knees", "bodyweight", "time", {
                "high": "45 seconds work, 15 seconds rest", 
                "moderate": "30 seconds work, 20 seconds rest", 
                "low": "20 seconds work, 20 seconds rest", 
                "recovery": "Avoid today"
            }],
            ["Skater Jumps", "bodyweight", "time", {
                "high": "45 seconds work, 15 seconds rest", 
                "moderate": "30 seconds work, 20 seconds rest", 
                "low": "20 seconds work, 20 seconds rest", 
                "recovery": "Avoid today"
            }],
            ["Squat Jumps", "bodyweight", "time", {
                "high": "45 seconds work, 15 seconds rest", 
                "moderate": "30 seconds work, 20 seconds rest", 
                "low": "20 seconds work, 20 seconds rest", 
                "recovery": "Avoid today"
            }]
        ],
        "mobility": [
            ["Cat-Cow Stretch", "bodyweight", "time", {
                "high": "3 sets of 10 repetitions", 
                "moderate": "3 sets of 8 repetitions", 
                "low": "2 sets of 8 repetitions", 
                "recovery": "2 sets of 5 repetitions"
            }],
            ["World's Greatest Stretch", "bodyweight", "time", {
                "high": "3 sets of 5 reps each side", 
                "moderate": "3 sets of 4 reps each side", 
                "low": "2 sets of 3 reps each side", 
                "recovery": "1 set of 3 reps each side"
            }],
            ["Child's Pose", "bodyweight", "time", {
                "high": "3 sets of 30 seconds", 
                "moderate": "3 sets of 30 seconds", 
                "low": "2 sets of 30 seconds", 
                "recovery": "1-2 sets of 30-45 seconds"
            }],
            ["Hip Flexor Stretch", "bodyweight", "time", {
                "high": "3 sets of 30 seconds each side", 
                "moderate": "3 sets of 30 seconds each side", 
                "low": "2 sets of 30 seconds each side", 
                "recovery": "1 set of 30-45 seconds each side"
            }],
            ["Foam Rolling", "equipment", "time", {
                "high": "1 minute per major muscle group", 
                "moderate": "45 seconds per major muscle group", 
                "low": "30 seconds per major muscle group", 
                "recovery": "1-2 minutes per tight muscle group"
            }]
        ]
    }
    
    # Get today's focus
    today_focus = focus_by_day[day_of_week]
    
    # Map the focus to the appropriate exercise category
    if "Push" in today_focus:
        primary_category = "upper_push"
        secondary_category = "core"
    elif "Pull" in today_focus:
        primary_category = "upper_pull"
        secondary_category = "core"
    elif "Lower Body" in today_focus:
        primary_category = "lower_body"
        secondary_category = "core"
    elif "Core" in today_focus:
        primary_category = "core"
        secondary_category = "mobility"
    elif "HIIT" in today_focus:
        primary_category = "hiit"
        secondary_category = "full_body"
    elif "Full Body" in today_focus:
        primary_category = "full_body"
        secondary_category = "core"
    else:  # Recovery & Mobility
        primary_category = "mobility"
        secondary_category = "core"
    
    # Select exercises based on intensity
    num_primary = 3 if intensity == "high" else 2 if intensity == "moderate" else 2 if intensity == "low" else 1
    num_secondary = 2 if intensity == "high" else 2 if intensity == "moderate" else 1 if intensity == "low" else 1
    
    # Randomly select exercises from the appropriate categories
    primary_exercises = random.sample(exercise_db[primary_category], min(num_primary, len(exercise_db[primary_category])))
    secondary_exercises = random.sample(exercise_db[secondary_category], min(num_secondary, len(exercise_db[secondary_category])))
    
    # Build the workout
    workout_text = ""
    
    # Add primary exercises
    workout_text += f"PRIMARY FOCUS ({primary_category.replace('_', ' ').title()}):\n"
    for ex in primary_exercises:
        name, equipment, format_type, details = ex
        if details[intensity] != "Avoid today":
            workout_text += f"• {name}: {details[intensity]}\n"
    
    # Add secondary exercises
    workout_text += f"\nSECONDARY FOCUS ({secondary_category.replace('_', ' ').title()}):\n"
    for ex in secondary_exercises:
        name, equipment, format_type, details = ex
        if details[intensity] != "Avoid today":
            workout_text += f"• {name}: {details[intensity]}\n"
    
    # If it's a HIIT day, add a circuit format suggestion
    if primary_category == "hiit" and intensity != "recovery":
        rounds = 4 if intensity == "high" else 3 if intensity == "moderate" else 2
        workout_text += f"\nComplete {rounds} rounds of the above exercises with minimal rest between exercises and 1-2 minutes rest between rounds."
    
    # Add cooldown for all workout types
    workout_text += "\nCOOLDOWN:\n• 5 minutes of light stretching focusing on worked muscle groups\n"
    
    # Return both the focus and the workout
    return {
        "focus": today_focus,
        "workout": workout_text
    }