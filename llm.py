"""LLM model inference utils"""

import json

from dotenv import dotenv_values
import boto3
from botocore.config import Config

# Set up the client

config = dotenv_values(".env")


AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS_SECRET_ACCESS_KEY")

MODEL_NAME = "amazon.titan-text-lite-v1"

config = Config(
    retries={
        "max_attempts": 8,
    }
)

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=config,
)


def llm_inference(prompt: str):
    """Call the Bedrock runtime API to get the response from the model

    Args:
        prompt (str): The prompt to send to the model

    Raises:
        ValueError: If the env vars are missing

    Returns:
        json_response (dict): The response from the model
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError(
            "Missing env variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
        )

    kwargs = {
        "modelId": MODEL_NAME,
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps({"inputText": prompt}),
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    json_response: dict = json.loads(response.get("body").read())

    return json_response
