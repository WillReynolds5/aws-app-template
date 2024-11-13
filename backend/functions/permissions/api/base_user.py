import json
import logging
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from functools import wraps
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get configuration from environment variables
region = os.environ.get(
    "AWS_REGION", "us-west-1"
)  # Fallback to us-west-1 for local development
user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
client_id = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")

if not user_pool_id or not client_id:
    raise ValueError(
        "Missing required environment variables: COGNITO_USER_POOL_ID and/or COGNITO_USER_POOL_CLIENT_ID"
    )


# CORS Headers
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token",
}


def get_public_key(token):
    jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    header = jwt.get_unverified_header(token)
    key = next((key for key in jwks["keys"] if key["kid"] == header["kid"]), None)
    if not key:
        raise ValueError("Public key not found")
    return RSAAlgorithm.from_jwk(json.dumps(key))


def validate_token(token):
    try:
        logger.info(
            f"Validating token: {token[:10]}..."
        )  # Log first 10 characters of token
        public_key = get_public_key(token)
        logger.info(f"Public Key: {public_key}")

        # First, decode without verification to check the token type
        unverified = jwt.decode(token, options={"verify_signature": False})
        token_use = unverified.get("token_use")
        logger.info(f"Token use: {token_use}")

        if token_use == "access":
            # For access tokens, verify without audience
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
                options={"verify_aud": False},
            )
            # Manually check client_id
            if decoded.get("client_id") != client_id:
                raise ValueError(
                    f"Invalid client_id. Expected {client_id}, got {decoded.get('client_id')}"
                )
        elif token_use == "id":
            # For ID tokens, verify with audience
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=client_id,
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
            )
        else:
            raise ValueError(f"Unknown token_use: {token_use}")

        logger.info(f"Decoded token: {json.dumps(decoded, indent=2)}")
        return decoded
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {str(e)}")
        raise ValueError(f"Token validation error: {str(e)}")


def extract_token(event):
    """
    Extract the token from various possible event structures.
    """
    # Try to get from the 'headers' key (common structure)
    headers = event.get("headers", {})
    if isinstance(headers, dict):
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if auth_header:
            return (
                auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
            )

    # Try to get from 'requestContext' (API Gateway structure)
    request_context = event.get("requestContext", {})
    authorizer = request_context.get("authorizer", {})
    if isinstance(authorizer, dict):
        return authorizer.get("token")

    # If we still can't find it, log the event structure and return None
    logger.error(f"Could not extract token from event: {json.dumps(event)}")
    return None


def base_user_handler(event, context):
    logger.info("Starting base_user_handler")
    logger.info(f"Event: {json.dumps(event)}")

    # Debug logging
    logger.debug(f"Event type: {type(event)}")
    logger.debug(f"Event keys: {event.keys()}")
    if "headers" in event:
        logger.debug(f"Headers: {json.dumps(event['headers'])}")

    # since this is a request authorizer, lets bypass option calls
    if event.get("httpMethod") == "OPTIONS":
        return generate_policy("user", "Allow", event["methodArn"])

    # Extract the Authorization header
    token = extract_token(event)

    if not token:
        logger.error("No token provided")
        return generate_policy("user", "Deny", event["methodArn"])

    try:
        decoded_token = validate_token(token)

        # Extract user ID from the decoded token
        user_id = decoded_token.get("sub", "Unknown")
        logger.info(f"Token validated for user: {user_id}")

        policy = generate_policy(user_id, "Allow", event["methodArn"])

        # Add custom context with user ID
        policy["context"] = {
            "user": user_id,
            "token": token,
        }

        return policy
    except ValueError as e:
        logger.error(f"Token validation failed: {str(e)}")
        return generate_policy("unauthorized", "Deny", event["methodArn"])


def generate_policy(principal_id, effect, resource):
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        },
    }
