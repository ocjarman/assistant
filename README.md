# Sleep and Wellness Assistant

A Python-based wellness assistant that helps track sleep patterns, provides daily workouts, and offers motivational content to support your health journey.

## Features

- **Sleep Tracking**: Integrates with Oura Ring to track and analyze your sleep patterns
- **Daily Workouts**: Generates personalized daily workout routines
- **Morning Reminders**: Delivers daily affirmations and motivational quotes
- **Automated Scheduling**: Runs on a schedule to provide timely updates and notifications
- **SMS Notifications**: Optional text message notifications via TextBelt

## Requirements

- Python 3.x
- Oura Ring and API access (for sleep tracking features)
- TextBelt API key (for SMS notifications)
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your API tokens and phone number:
     ```
     OURA_API_TOKEN=your_oura_token_here
     TEXTBELT_API_KEY=your_textbelt_key_here
     PHONE_NUMBER=your_phone_number  # Format: 1234567890 (no spaces or special characters)
     ```

### Setting up TextBelt (Optional)

If you want to receive SMS notifications:
1. Visit [TextBelt](https://textbelt.com/) to get an API key
   - They offer both paid plans and a free tier (250 texts per month)
   - Test key available: Use `textbelt_test` (limited to 1 message per day)
2. Add your TextBelt API key to the `.env` file as shown above
3. Add your phone number to receive notifications
   - Use only numbers, no spaces or special characters
   - For US numbers, use format: 1234567890
   - For international numbers, include country code: 441234567890

## Usage

Run the main script:
```bash
python sleep.py
```

The program will:
- Track sleep data (pulls from Oura Ring at 7:00 AM daily)
- Generate daily workouts (available at 9:15 AM)
- Provide morning reminders with affirmations and quotes (at 9:15 AM)

## Project Structure

- `sleep.py`: Main script that runs the scheduling system
- `utils/`
  - `oura.py`: Handles Oura Ring API integration
  - `sleepUtils.py`: Sleep data processing and analysis
  - `workouts.py`: Workout generation and management
  - `quotes.py`: Affirmations and motivational content
  - `print.py`: Formatting and display utilities

## Configuration

The schedule can be modified in `sleep.py`. By default:
- Sleep data collection: 7:00 AM
- Daily workout generation: 9:15 AM
- Morning reminders: 9:15 AM

## Data Storage

Sleep history is stored in `sleep_history.txt` for tracking and analysis purposes.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
