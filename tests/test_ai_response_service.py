import unittest
from unittest.mock import patch
from domain.services.ai_response_servidce import AIResponseService
from domain.entities.ai_response import AIResponse

class TestAIResponseService(unittest.TestCase):
    @patch('domain.services.ai_response_servidce.BedrockClient')
    def test_generate_response(self, MockBedrockClient):
        mock_client = MockBedrockClient.return_value
        mock_client.query_claude_with_profile.return_value = "テスト応答"

        service = AIResponseService()
        response = service.generate_response("テストプロンプト")

        self.assertIsInstance(response, AIResponse)
        self.assertEqual(response.content, "テスト応答")

    def test_load_system_prompt(self):
        service = AIResponseService()
        with patch('builtins.open', unittest.mock.mock_open(read_data="システムプロンプト")):
            system_prompt = service.load_system_prompt("dummy_path")
            self.assertEqual(system_prompt, "システムプロンプト")

if __name__ == '__main__':
    unittest.main()
