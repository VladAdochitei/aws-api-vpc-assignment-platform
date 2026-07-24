# Region Locks

## Overview

All VPC and Subnet operations are restricted to a single AWS region. This restriction is enforced at the boto3 EC2 client level.

## How It Works

The EC2 client is initialized with a region from the `AWS_REGION` environment variable at startup:

**File:** `src/controllers/services/boto_ec2/base_ec2.py:4`

```python
_ec2 = boto3.client("ec2", region_name=os.environ.get("AWS_REGION"))
```

This single client instance is reused for all EC2 operations (VPC creation, subnet creation, deletion, etc.). Since it's locked to a specific region, all operations happen in that region only.

## Region Configuration

- **Development/Lambda Environment:** Set `AWS_REGION` environment variable before deploying Lambda functions
- **Local Testing:** Export `AWS_REGION` in your shell session:
  ```bash
  export AWS_REGION="eu-central-1"
  ```
- **Terraform Deployment:** Configured in infrastructure variables

## Impact

- **VPC Creation:** VPCs are always created in the configured region
- **Subnet Creation:** Subnets can only be created in availability zones within the configured region
- **No Multi-Region Support:** The current design does not support multi-region deployments without code changes

## Changing the Region

To support a different region:

1. Update the `AWS_REGION` environment variable where Lambda functions are deployed
2. Update local dev environment if testing locally
3. No code changes needed — the region is purely environment-driven

## Why This Approach

- **Simplicity:** Single region simplifies infrastructure management and API Gateway configuration
- **Cost:** Avoids unnecessary cross-region data transfer
- **Compliance:** Region-locked deployments can help meet data residency requirements
