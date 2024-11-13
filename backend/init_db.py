import boto3
import os
import uuid
import random
from datetime import datetime, timezone
import requests
from botocore.exceptions import ClientError

# Set up DynamoDB client
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

# Set up S3 client (non-local, staging)
s3 = boto3.client("s3")

TABLE_NAME = os.environ.get("TABLE_NAME", "MeecaApp")
BUCKET_NAME = "meeca2-dev"

# Sample data
names = ["Alice", "Mia", "Kelce"]
personalities = ["Friendly", "Mysterious", "Energetic", "Calm", "Witty", "Adventurous"]
image_urls = [
    "https://i.ibb.co/GcfBRZT/3.jpg",
    "https://i.ibb.co/XyT3W62/GTEjn-El-XQAAVt80.jpg",
]


def create_table():
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GSI1PK", "AttributeType": "S"},
                {"AttributeName": "GSI1SK", "AttributeType": "S"},
                {"AttributeName": "GSI2PK", "AttributeType": "S"},
                {"AttributeName": "GSI2SK", "AttributeType": "S"},
                {"AttributeName": "OwnerId", "AttributeType": "S"},  # Include OwnerId
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GSI1PK-GSI1SK-index",
                    "KeySchema": [
                        {"AttributeName": "GSI1PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "GSI2PK-GSI2SK-index",
                    "KeySchema": [
                        {"AttributeName": "GSI2PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI2SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "OwnerId-index",  # New index for OwnerId
                    "KeySchema": [
                        {"AttributeName": "OwnerId", "KeyType": "HASH"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
            ],
        )
        table.wait_until_exists()
        print("Table created successfully.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table {TABLE_NAME} already exists. Skipping table creation.")
            table = dynamodb.Table(TABLE_NAME)
        else:
            raise e
    return table


def generate_avatar():
    avatar_id = str(uuid.uuid4())
    name = random.choice(names)
    names.remove(name)
    personality = random.choice(personalities)
    image_url = random.choice(image_urls)

    response = requests.get(image_url)
    img_data = response.content

    image_id = str(uuid.uuid4())
    image_key = f"{avatar_id}/{image_id}.png"
    s3.put_object(Bucket=BUCKET_NAME, Key=image_key, Body=img_data)
    s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_key}"

    description = f"A {random.choice(['vibrant', 'mysterious', 'charming', 'elegant'])} image of {name}"

    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        # HASH / RANGE properties
        "PK": f"AVATAR#{avatar_id}",
        "SK": timestamp,
        "GSI1PK": "active",
        "GSI1SK": timestamp,
        # Other attributes
        "Id": avatar_id,
        "AvatarName": name,
        "Personality": personality.strip(),
        "AvatarStatus": "active",
        "Images": [{"link": s3_url, "description": description}],
        "CreatedAt": timestamp,
        "UpdatedAt": timestamp,
        "EntityType": "Avatar",
    }


def main():
    # Create the table or get existing table
    table = create_table()

    # Generate and add avatars
    for _ in range(2):  # Generate 2 avatars
        avatar_data = generate_avatar()
        table.put_item(Item=avatar_data)
        print(f"Added avatar: {avatar_data['AvatarName']} (ID: {avatar_data['Id']})")
        print(f"Image URL: {avatar_data['Images'][0]['link']}")

        # Verify data insertion
        response = table.get_item(
            Key={"PK": avatar_data["PK"], "SK": avatar_data["SK"]}
        )
        print("Retrieved item:", response.get("Item"))

    # After adding avatars, list all tables to verify
    existing_tables = list(dynamodb.tables.all())
    print(f"Existing tables: {[table.name for table in existing_tables]}")


if __name__ == "__main__":
    main()
