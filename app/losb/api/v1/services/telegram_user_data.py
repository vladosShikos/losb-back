import requests


def get_telegram_user_data(telegram_id: int, bot_token: str):
    """
    Get user data from Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getChat?chat_id={telegram_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise ValueError("Failed to get user data from Telegram.")

        user_data = data["result"]
        return {
            "first_name": user_data.get("first_name", ""),
            "last_name": user_data.get("last_name", ""),
            "username": user_data.get("username", "")
        }
    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred while getting user data from Telegram: {e}")
        return {"first_name": "", "last_name": "", "username": ""}
