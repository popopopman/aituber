from infrastructure.bedrock_client import BedrockClient
from domain.entities.ai_response import AIResponse

class AIResponseService:
    def __init__(self):
        self.bedrock_client = BedrockClient()

    def generate_response(self, prompt):
        response_text = self.bedrock_client.query_claude(prompt)
        return AIResponse(response_text)