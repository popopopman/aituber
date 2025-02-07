import json
import unittest
from unittest.mock import patch, MagicMock
from infrastructure.bedrock_client import BedrockClient


class TestBedrockClient(unittest.TestCase):
    @patch("infrastructure.bedrock_client.boto3.client")
    def test_query_claude_with_profile(self, MockBotoClient):
        mock_client = MockBotoClient.return_value
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"content": [{"type": "text", "text": "テスト応答"}]}).encode(
            "utf-8"
        )
        mock_client.invoke_model.return_value = {"body": mock_response}

        client = BedrockClient()
        response = client.query_claude_with_profile("test_model_arn", "テストプロンプト")

        self.assertEqual(response, "テスト応答")

    @patch("infrastructure.bedrock_client.boto3.client")
    def test_query_claude_with_profile_no_response(self, MockBotoClient):
        mock_client = MockBotoClient.return_value
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"content": []}).encode("utf-8")
        mock_client.invoke_model.return_value = {"body": mock_response}

        client = BedrockClient()
        response = client.query_claude_with_profile("test_model_arn", "テストプロンプト")

        self.assertEqual(response, "No response")

    @patch("infrastructure.bedrock_client.boto3.client")
    def test_query_claude_with_profile_exception(self, MockBotoClient):
        mock_client = MockBotoClient.return_value
        mock_client.invoke_model.side_effect = Exception("Test exception")

        client = BedrockClient()
        response = client.query_claude_with_profile("test_model_arn", "テストプロンプト")

        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
