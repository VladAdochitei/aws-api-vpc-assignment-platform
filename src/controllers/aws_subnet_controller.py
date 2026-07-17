import json


def list_subnets(event):
    dummy_subnets = [
        {"subnet_id": "subnet-00000001", "vpc_id": "vpc-00000001", "cidr_block": "10.0.1.0/24"},
        {"subnet_id": "subnet-00000002", "vpc_id": "vpc-00000002", "cidr_block": "10.1.1.0/24"},
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"subnets": dummy_subnets}),
    }