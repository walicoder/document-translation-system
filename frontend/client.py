import requests
import httpx

BASE_URL = "http://localhost:8000"

# URL = "http://127.0.0.1:8000/translate/"


def validate_user(username: str, password: str) -> bool:
    url = f"{BASE_URL}/validate-user"
    payload = {
        "username": username,
        "password": password
    }
    with httpx.Client() as client:
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            return True
        except httpx.HTTPStatusError as e:
            print(e)
            return False


def get_translations(username: str):
    url = f"{BASE_URL}/users/{username}/translations/"
    with httpx.Client() as client:
        try:
            response = client.get(url)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            return response.json()
        except httpx.HTTPStatusError as e:
            print(e)
            return []


def get_translations_batch(username: str):
    url = f"{BASE_URL}/users/{username}/translations-batch/"
    with httpx.Client() as client:
        try:
            response = client.get(url)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            return response.json()
        except httpx.HTTPStatusError as e:
            print(e)
            return []


def post_translation(username: str, english_text: str, bengali_text: str, session_id: str):
    url = f"{BASE_URL}/users/{username}/translations/"
    payload = {
        "english_text": english_text,
        "bengali_text": bengali_text,
        "session_id": session_id
    }
    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()


def post_translation_batch(username: str, english_text: str, bengali_text: str, session_id: str):
    url = f"{BASE_URL}/users/{username}/translations-batch/"
    payload = {
        "english_text": english_text,
        "bengali_text": bengali_text,
        "session_id": session_id
    }
    with httpx.Client() as client:
        response = client.post(url, json=payload)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()


def translate(text: str):
    url = f"{BASE_URL}/translate"
    response = requests.get(url, params={"text": text})
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}


def split_n_translate(text: str):
    url = f"{BASE_URL}/translate-batch"
    response = requests.get(url, params={"text": text})
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}


if __name__ == "__main__":
    # validation_response = validate_user("walima", "123456")
    # print("Validation response:", validation_response)

    # Get all translations for the user
    # get_response = get_translations("walima")
    # print("Get response:", get_response)
    print(translate("আন্দোলন দমনে পুলিশ ১৪৪ ধারা জারি করে ঢাকা শহরে মিছিল"))
    print(split_n_translate("বাংলাদেশের ভাষা আন্দোলন আমাদের ইতিহাসের একটি গৌরবময় অধ্যায় । ১৯৫২ সালের ২১শে ফেব্রুয়ারি বাংলাভাষাকে রাষ্ট্রভাষা হিসেবে স্বীকৃতি দেওয়ার দাবিতে ঢাকার ছাত্র-জনতা আন্দোলনে নামে ।"))