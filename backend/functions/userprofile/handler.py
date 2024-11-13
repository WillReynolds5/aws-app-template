import os
import json
import logging
from get import user_profile_get
from create import user_profile_create

logger = logging.getLogger()
logger.setLevel(logging.INFO)

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
}

unsupported_response = {
    "statusCode": 400,
    "headers": headers,
    "body": json.dumps({"error": "Unsupported HTTP method or path"}),
}


def user_profile_handler(event, context):
    http_method = event["httpMethod"]
    path = event["path"]

    # Handle CORS preflight request# Handle CORS preflight request
    if http_method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    # Remove trailing slash for consistent path matching
    path = path.rstrip("/")

    logger.info(f"Received request: {http_method} {path}")

    try:
        response = None
        if http_method == "GET" and path == "/user-profile":
            response = user_profile_get(event, context)
        elif http_method == "POST" and path == "/user-profile":
            response = user_profile_create(event, context)

        # Add headers to the response if a handler was called
        if response:
            response["headers"] = headers
            return response

        return unsupported_response

    except Exception as e:
        logger.error(
            f"Error in user_profile_handler for {http_method} {path}: {str(e)}"
        )
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)}),
        }
