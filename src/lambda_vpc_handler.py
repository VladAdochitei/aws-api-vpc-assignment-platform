from controllers.aws_vpc_controller import list_vpcs #, create_vpc, get_vpc, update_vpc, delete_vpc

ROUTES = {
    ("GET", "/vpcs"): list_vpcs,
    # ("POST", "/vpcs"): create_vpc,
    # ("GET", "/vpcs/{vpc_id}"): get_vpc,
    # ("PUT", "/vpcs/{vpc_id}"): update_vpc,
    # ("DELETE", "/vpcs/{vpc_id}"): delete_vpc,
}

def api_handler(event, context):
    print(event)
    key = (event["httpMethod"], event["resource"])
    fn = ROUTES.get(key)
    if not fn:
        return {"statusCode": 404, "body": '{"message": "not found"}'}
    return fn(event)