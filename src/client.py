import requests

URL = "http://127.0.0.1:8000/translate/"


def send_get_request(text: str):
    response = requests.get(URL, params={"text": text})
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}


if __name__ == "__main__":
    print(send_get_request("আন্দোলন দমনে পুলিশ ১৪৪ ধারা জারি করে ঢাকা শহরে মিছিল"))
