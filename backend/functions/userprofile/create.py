import arrow
import os
import logging
import json
import boto3


is_local = "AWS_SAM_LOCAL" in os.environ

if is_local:
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb-local:8000")
else:
    dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "MeecaApp")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def user_profile_create(event, context):

    try:
        body = json.loads(event["body"]) if event["body"] else {}

        user_id = body["user_id"]
        email = body.get("email")
        name = body.get("name")
        timestamp = arrow.utcnow().isoformat()

        table = dynamodb.Table(TABLE_NAME)
        item = {
            # HASH / RANGE properties
            "PK": f"USER#{user_id}",
            "SK": timestamp,
            "GSI2PK": f"EMAIL#{email}",
            "GSI2SK": f"{timestamp}",
            "GSI1SK": f"UPDATED_AT#{timestamp}",
            # Other attributes
            "Id": user_id,
            "Email": email,
            "FirstName": name,
            "Status": "active",
            "CreatedAt": timestamp,
            "UpdatedAt": timestamp,
            "EntityType": "UserProfile",
        }
        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User profile created successfully"}),
        }
    except Exception as e:
        logger.error(f"Error in user_profile_post_handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error: {str(e)}"}),
        }
