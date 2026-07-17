from controllers.aws_subnet_controller import (
    list_subnets #, create_subnet, get_subnet, update_subnet, delete_subnet,
    # list_subnets_by_vpc, create_subnet_for_vpc,
)

ROUTES = {
    ("GET", "/subnets"): list_subnets,
    # ("GET", "/subnets/{subnet_id}"): get_subnet,
    # ("PUT", "/subnets/{subnet_id}"): update_subnet,
    # ("DELETE", "/subnets/{subnet_id}"): delete_subnet,
    # ("GET", "/vpcs/{vpc_id}/subnets"): list_subnets_by_vpc,
    # ("POST", "/vpcs/{vpc_id}/subnets"): create_subnet_for_vpc,
}

def api_handler(event, context):
    print(event)
    key = (event["httpMethod"], event["resource"])
    fn = ROUTES.get(key)
    if not fn:
        return {"statusCode": 404, "body": '{"message": "not found"}'}
    return fn(event)