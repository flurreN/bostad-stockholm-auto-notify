import requests
import os

class DiscordInfrastructure:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        full_message = {"content": message}
        requests.post(self.webhook_url, json=full_message, timeout=5)
