import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
}


def create_initial_prompt(event, context):
    try:
        body = json.loads(event["body"]) if event["body"] else {}
        prompt_text = body.get("prompt")

        if not prompt_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Prompt text is required"}),
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Prompt received", "prompt": prompt_text}),
        }

    except Exception as e:
        logger.error(f"Error in create_initial_prompt: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }


def prompt_handler(event, context):
    http_method = event["httpMethod"]
    path = event["path"]

    # Handle CORS preflight request
    if http_method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    path = path.rstrip("/")
    logger.info(f"Received request: {http_method} {path}")

    try:
        response = None
        if http_method == "POST" and path == "/prompt":
            response = create_initial_prompt(event, context)

        if response:
            response["headers"] = headers
            return response

        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Unsupported HTTP method or path"}),
        }

    except Exception as e:
        logger.error(f"Error in prompt_handler: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)}),
        }
