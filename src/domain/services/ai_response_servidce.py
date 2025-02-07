import sys
import os

from infrastructure.bedrock_client import BedrockClient
from domain.entities.ai_response import AIResponse
from config import MODEL_ARN

class AIResponseService:
    def __init__(self):
        """
        AIResponseService クラスのコンストラクタ。
        """
        self.bedrock_client = BedrockClient()

    def generate_response(self, prompt: str, system_prompt: str = None) -> AIResponse:
        """
        指定されたプロンプトに対する AI 応答を生成する。
        
        :param prompt: ユーザーからのプロンプト
        :param system_prompt: システムプロンプト (オプション)
        :return: AIResponse オブジェクト
        """
        response_text = self.bedrock_client.query_claude_with_profile(MODEL_ARN, prompt, system_prompt)
        return AIResponse(response_text)

    def load_system_prompt(self, file_path: str) -> str:
        """
        指定されたファイルからシステムプロンプトを読み込む。
        
        :param file_path: システムプロンプトが記述されたファイルのパス
        :return: システムプロンプトの内容
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()