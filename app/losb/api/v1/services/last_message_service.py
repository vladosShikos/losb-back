import requests
from django.conf import settings
from datetime import datetime


class LastMessageService:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.bot_token = settings.TECHSUPPORT_BOT_TOKEN
        self.relative_avatar_url = 'images/default_avi.png'

    def get_last_message(self):
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        try:
            response = requests.get(url, params={'offset': 0})
            response.raise_for_status()
            data = response.json()

            if not data.get("ok"):
                return None, "Failed to get updates from Telegram."

            messages = data.get("result", [])

            last_message_info = None
            for message in reversed(messages):
                user_message = message.get('message', {})
                user_id = user_message.get('from', {}).get('id')

                if str(user_id) == self.telegram_id:

                    message_text = user_message.get('text')
                    timestamp = user_message.get('date')

                    if message_text and timestamp:
                        formatted_time = datetime.fromtimestamp(timestamp).strftime('%H:%M')
                        last_message_info = {
                            'message': message_text,
                            'time': formatted_time
                        }
                        break

            return last_message_info, None
        except requests.RequestException as e:
            return None, str(e)

    def get_avatar_url(self):
        return f"{settings.MEDIA_URL}{self.relative_avatar_url}"
