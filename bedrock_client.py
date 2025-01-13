import json
import boto3
import botocore
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class BedrockClient:
    """
    AWS Bedrock Runtime クライアント
    bedrockで提供されているモデルとやり取りを行う
    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        """
        :param aws_access_key_id: AWS アクセスキー
        :param aws_secret_access_key: AWS シークレットキー
        :param region_name: リージョン名 (例: 'ap-northeast-1')
        """
        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def query_claude_with_profile(self, inference_profile_arn, prompt, max_tokens=1000):
        """
        Claude に問い合わせるためのメソッド。
        :param inference_profile_arn: Claude の推論プロファイルのARN
        :param prompt: モデルに送るプロンプト
        :param max_tokens: 生成トークン数の上限
        :return: モデルからの応答テキスト
        """
        try:
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )

            response = self.client.invoke_model(
                modelId=inference_profile_arn, body=body, contentType="application/json", accept="application/json"
            )
            response_body = json.loads(response["body"].read())
            return response_body.get("content", "No response")
        except Exception as e:
            logger.error(f"Error querying Claude: {e}")
            return None
