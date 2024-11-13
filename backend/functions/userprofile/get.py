import logging
import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Check if we're running locally
is_local = "AWS_SAM_LOCAL" in os.environ

# Set up DynamoDB resource
if is_local:
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb-local:8000")
else:
    dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "MeecaApp")


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def user_profile_get(event, context):
    logger.info("Starting user_profile_get")

    # Extract user ID from the authorizer context
    try:
        user_id = event["requestContext"]["authorizer"]["user"]
        logger.info(f"User ID extracted from authorizer context: {user_id}")
    except KeyError:
        logger.error("User ID not found in the authorizer context")
        logger.debug(f"Event context: {json.dumps(event['requestContext'])}")
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Unauthorized: User ID not found"}),
        }

    logger.info(f"table name: {TABLE_NAME}")
    table = dynamodb.Table(TABLE_NAME)
    logger.info(f"Table: {table}")
    response = table.query(KeyConditionExpression=Key("PK").eq(f"USER#{user_id}"))

    logger.info(f"Response: {response}")
    if response["Items"]:
        user_profile = response["Items"][0]

        # Filter the user profile to include only the requested fields
        filtered_profile = {
            "email": user_profile.get("Email", ""),
            "first_name": user_profile.get("FirstName", ""),
        }

        return {
            "statusCode": 200,
            "body": json.dumps(filtered_profile, default=decimal_default),
        }
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "User profile not found"}),
        }
