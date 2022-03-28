from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


def create_answer(message_text):
    if message_text in ["oi", "olá", "eai"]:
        return "Olá, tudo bem?"
    else:
        return "Não entendi!"


class TelegramBot:
    def __init__(self):
        token = os.getenv("API_KEY")  # get token from .env file
        self.url = f"https://api.telegram.org/bot{token}/"

    def start(self):
        update_id = None
        while True:
            update = self.get_messages(update_id)
            messages = update['result']
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        message_text = message['message']['text']
                        answer_bot = create_answer(message_text)
                        self.send_answer(chat_id, answer_bot)
                    except:
                        pass

    def get_messages(self, update_id):
        link_request = f"{self.url}getUpdates?timeout=1000"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout=1000&offset={update_id + 1}"
        result = requests.get(link_request)
        return json.loads(result.content)

    def send_answer(self, chat_id, answer):
        link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text{answer}"
        requests.get(link_to_send)
        return
