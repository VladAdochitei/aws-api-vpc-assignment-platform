#!/usr/bin/env python3
import sys
import os
from services.api_client import APIClient

API_KEY = "dev-local-key-CHANGE-ME"
BASE_URL = os.getenv('API_BASE_URL', "https://<api-key-identifier>.execute-api.eu-central-1.amazonaws.com/dev")

def test_workflow():
    print(f"Running integration tests against {BASE_URL}")
    print(f"Using API key: {API_KEY}\n")

    client = APIClient(base_url=BASE_URL, api_key=API_KEY)

    # Test 1: List VPCs
    print("1. Testing list_vpcs...")
    try:
        result = client.list_vpcs()
        print(f"✓ list_vpcs returned {result['count']} VPCs")
    except Exception as e:
        print(f"✗ list_vpcs failed: {e}")
        return False

    # Test 2: Create a VPC
    print("\n2. Testing create_vpc...")
    try:
        vpc_result = client.create_vpc(
            vpc_name="test-vpc-integration",
            cidr_block="10.0.0.0/16",
            region="eu-central-1"
        )
        vpc_id = vpc_result['vpc_id']
        print(f"✓ create_vpc returned vpc_id: {vpc_id}")
    except Exception as e:
        print(f"✗ create_vpc failed: {e}")
        return False

    # Test 3: Get the VPC we just created
    print("\n3. Testing get_vpc with created vpc_id...")
    try:
        get_result = client.get_vpc(vpc_id)
        assert get_result['vpc_id'] == vpc_id
        assert get_result['vpc_name'] == "test-vpc-integration"
        print(f"✓ get_vpc returned: {get_result['vpc_name']}")
    except Exception as e:
        print(f"✗ get_vpc failed: {e}")
        return False

    # Test 4: Update the VPC
    print("\n4. Testing update_vpc...")
    try:
        update_result = client.update_vpc(vpc_id, vpc_name="test-vpc-updated")
        assert update_result['vpc_name'] == "test-vpc-updated"
        print(f"✓ update_vpc returned: {update_result['vpc_name']}")
    except Exception as e:
        print(f"✗ update_vpc failed: {e}")
        return False

    # Test 5: List subnets (should be empty for new VPC)
    print("\n5. Testing list_subnets_by_vpc...")
    try:
        subnets_result = client.list_subnets_by_vpc(vpc_id)
        print(f"✓ list_subnets_by_vpc returned {subnets_result['count']} subnets")
    except Exception as e:
        print(f"✗ list_subnets_by_vpc failed: {e}")
        return False

    # Test 6: Create a subnet in the VPC
    print("\n6. Testing create_subnet...")
    try:
        subnet_result = client.create_subnet(
            vpc_id=vpc_id,
            subnet_name="test-subnet",
            cidr_block="10.0.1.0/24",
            availability_zone="eu-central-1a"
        )
        subnet_id = subnet_result['subnet_id']
        assert subnet_result['vpc_id'] == vpc_id
        print(f"✓ create_subnet returned subnet_id: {subnet_id}")
    except Exception as e:
        print(f"✗ create_subnet failed: {e}")
        return False

    # Test 7: Get the subnet we just created
    print("\n7. Testing get_subnet with created subnet_id...")
    try:
        get_subnet_result = client.get_subnet(subnet_id)
        assert get_subnet_result['subnet_id'] == subnet_id
        assert get_subnet_result['subnet_name'] == "test-subnet"
        print(f"✓ get_subnet returned: {get_subnet_result['subnet_name']}")
    except Exception as e:
        print(f"✗ get_subnet failed: {e}")
        return False

    # Test 8: Update the subnet
    print("\n8. Testing update_subnet...")
    try:
        update_subnet_result = client.update_subnet(subnet_id, subnet_name="test-subnet-updated")
        assert update_subnet_result['subnet_name'] == "test-subnet-updated"
        print(f"✓ update_subnet returned: {update_subnet_result['subnet_name']}")
    except Exception as e:
        print(f"✗ update_subnet failed: {e}")
        return False

    # Test 9: List all subnets
    print("\n9. Testing list_subnets...")
    try:
        all_subnets = client.list_subnets()
        print(f"✓ list_subnets returned {all_subnets['count']} total subnets")
    except Exception as e:
        print(f"✗ list_subnets failed: {e}")
        return False

    # Test 10: Delete the subnet
    print("\n10. Testing delete_subnet...")
    try:
        delete_subnet_result = client.delete_subnet(subnet_id)
        print(f"✓ delete_subnet: {delete_subnet_result['message']}")
    except Exception as e:
        print(f"✗ delete_subnet failed: {e}")
        return False

    # Test 11: Delete the VPC
    print("\n11. Testing delete_vpc...")
    try:
        delete_vpc_result = client.delete_vpc(vpc_id)
        print(f"✓ delete_vpc: {delete_vpc_result['message']}")
    except Exception as e:
        print(f"✗ delete_vpc failed: {e}")
        return False

    print(f"\n{'='*50}")
    print("✓ All integration tests passed!")
    return True

if __name__ == '__main__':
    success = test_workflow()
    sys.exit(0 if success else 1)
