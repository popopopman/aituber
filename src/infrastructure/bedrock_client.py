import json
import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BedrockClient:
    """
    AWS Bedrock Runtime クライアント
    bedrockで提供されているモデルとやり取りを行う
    """

    def __init__(self):
        """
        BedrockClient クラスのコンストラクタ。
        """
        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )

    def query_claude_with_profile(self, model_arn: str, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """
        Claude に問い合わせるためのメソッド。
        
        :param model_arn: Claude のモデルのARN
        :param prompt: モデルに送るプロンプト
        :param system_prompt: システムプロンプト (オプション)
        :param max_tokens: 生成トークン数の上限
        :return: モデルからの応答テキスト
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "assistant", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": messages,
                }
            )

            response = self.client.invoke_model(
                modelId=model_arn, body=body, contentType="application/json", accept="application/json"
            )
            response_body = json.loads(response["body"].read())

            # 生成されたテキストを取得
            content = response_body.get("content", [])
            if content and isinstance(content, list):
                text = "".join([part.get("text", "") for part in content if part.get("type") == "text"])
            else:
                text = "No response"

            logger.info(f"コメント: {prompt}")
            logger.info(f"回答: {text}")

            return text
        except Exception as e:
            logger.error(f"Error querying Claude: {e}")
            return None
