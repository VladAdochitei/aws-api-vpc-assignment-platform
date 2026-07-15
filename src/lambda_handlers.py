import os


def hello_world_handler(event, context):
    environment = os.environ.get("ENVIRONMENT", "not set")
    print("Hello, World!")
    print(f"ENVIRONMENT={environment}")

    return {
        "statusCode": 200,
        "body": f"Hello, World! ENVIRONMENT={environment}",
    }

