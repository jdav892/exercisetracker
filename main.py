import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv(f"Your.env")
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
EXERCISE_ENDPOINT = os.environ.get("EXERCISE_ENDPOINT")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

GENDER = "Your Gender"
WEIGHT_KG = "Your weight in kg as a float" 
HEIGHT_CM = "Your height in cm as an int" 
AGE = "Your age as an int" 




exercise_endpoint = EXERCISE_ENDPOINT
sheet_endpoint = SHEET_ENDPOINT



exercise_text = input("Which exercise did you perform?:")

exercise_config = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
exercise_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_response = requests.post(
    url=exercise_endpoint,
    json=exercise_config,
    headers=exercise_header)
exercise_response.raise_for_status()
exercise_data = exercise_response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")



for exercise in exercise_data["exercises"]:
    sheet_config = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

bearer_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

sheet_response = requests.post(
    sheet_endpoint, 
    json=sheet_config,
    headers=bearer_headers)
sheet_response.raise_for_status()
print(sheet_response.text)