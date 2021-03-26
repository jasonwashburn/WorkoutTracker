import requests
import os
import datetime as dt

NUTRITIONIX_ID = os.getenv("NUTRITIONIX_ID")
NUTRITIONIX_KEY = os.getenv("NUTRITIONIX_KEY")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")


def process_user_exercise(exercise_string):
    """
    Converts a plain text string describing a workout and converts it into data formatted for our spreadsheet
    :param exercise_string: a plain text string describing a workout
    :return: returns a json list of workout data
    """
    headers = {
        "x-app-id": NUTRITIONIX_ID,
        "x-app-key": NUTRITIONIX_KEY,
        'Content-Type': "application/json"
    }

    parameters = {
        "query": exercise_string,
        "gender": "male",
        "weight_kg": 85,
        "height_cm": 190.5,
        "age": 41
    }

    response = requests.post('https://trackapi.nutritionix.com/v2/natural/exercise', json=parameters, headers=headers)
    processed_list = []

    for workout in response.json()['exercises']:
        workout_dict = {
            'date': dt.datetime.now().strftime("%d/%m/%Y"),
            'time': dt.datetime.now().strftime("%X"),
            'exercise': str.title(workout['name']),
            'duration': workout['duration_min'],
            'calories': workout['nf_calories']
        }
        processed_list.append(workout_dict)
    return processed_list


def to_sheety(workout_dict):
    """
    Sends the workout data to our google sheet
    :param workout_dict: a dictionary properly formatted for pushing to google sheets
    :return: None
    """
    headers = {
        "Authorization": f"Bearer {SHEETY_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(SHEETY_ENDPOINT, json=workout_dict, headers=headers)
    print(response.json())


user_input = input("What exercise(s) did you do? ")
converted_workouts = process_user_exercise(user_input)

for item in converted_workouts:
    payload = {'workout': item}
    to_sheety(payload)
