import unittest
from unittest.mock import Mock, patch
from src.infrastructure.discord import DiscordInfrastructure

class TestDiscordInfrastructure(unittest.TestCase):
    def setUp(self):
        # Mock the requests.post method to prevent actual HTTP requests
        self.mock_requests = Mock()
        self.patcher = patch('src.infrastructure.discord.requests.post', new=self.mock_requests)
        self.patcher.start()

        self.webhook_url = 'https://example.com/webhook'
        self.discord = DiscordInfrastructure(self.webhook_url)

    def tearDown(self):
        # Stop the patcher to clean up
        self.patcher.stop()

    def test_send_messege(self):
        message = "Test message"
        self.discord.send_messege(message)

        # Check that requests.post was called with the expected arguments
        self.mock_requests.assert_called_once_with(self.webhook_url, json={"content": message}, timeout=5)

if __name__ == '__main__':
    unittest.main()
