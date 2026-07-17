# Should use the models from the models package instead of importing them directly from the files
# Should have available methods such as:
# - list_vpcs()
# - create_vpc(vpc_id, vpc_name, cidr_block, region, created_by)
# - get_vpc_by_id(vpc_id)
# - update_vpc(vpc_id, vpc_name=None, cidr_block=None, region=None, status=None)
# - delete_vpc(vpc_id)
# Should also talk to the database using SQLAlchemy and handle exceptions appropriately, should also perform API calls with boto3.

import json


def list_vpcs(event):
    dummy_vpcs = [
        {"vpc_id": "vpc-00000001", "cidr_block": "10.0.0.0/16", "name": "dummy-vpc-1"},
        {"vpc_id": "vpc-00000002", "cidr_block": "10.1.0.0/16", "name": "dummy-vpc-2"},
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"vpcs": dummy_vpcs}),
    }