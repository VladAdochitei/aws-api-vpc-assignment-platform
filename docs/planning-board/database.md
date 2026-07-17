# Database Strategy

## Requirement
Cheap database for PoC. Durability not critical for MVP.

## AWS Database Options for PoC

### 1. Aurora Serverless v2
- **Cost:** Scales to zero when not in use → nearly free during development
- **Setup:** ~10 minutes
- **SQL:** Yes (PostgreSQL or MySQL compatible)
- **Pros:** Serverless, cheap, familiar SQL, scales automatically
- **Cons:** Small cold start latency (~1-2 seconds after idle period)

### 2. RDS Free Tier
- **Cost:** Free for 12 months (db.t3.micro, 20GB), then ~$0.15/hour
- **Setup:** ~5 minutes
- **SQL:** Yes (PostgreSQL or MySQL)
- **Pros:** Fully managed, straightforward, most familiar
- **Cons:** Costs money even when idle

### 3. DynamoDB
- **Cost:** Free tier (25GB, 1M requests/month), then pay-per-request
- **Setup:** ~2 minutes
- **SQL:** No (NoSQL)
- **Pros:** Serverless, scales to zero, minimal infrastructure
- **Cons:** Not SQL, different query patterns, requires NoSQL design

### 4. SQLite + S3
- **Cost:** Essentially free (just S3 storage cents)
- **Setup:** ~15 minutes
- **SQL:** Yes
- **Pros:** Minimal infrastructure, super cheap
- **Cons:** Concurrency issues with Lambda, manual file management

## Decision: DynamoDB

**CHOSEN APPROACH** for this project:
- DynamoDB with two-table design (vpcs, subnets)
- True serverless: no database instance to manage or pay for when idle
- Pay-per-request pricing: free tier covers PoC traffic entirely
- NoSQL model works well with Lambda's stateless execution

### Why DynamoDB
1. **Cost:** Free tier covers PoC usage; true scale-to-zero (Aurora v2 minimum = ~$43/month)
2. **Serverless:** No VPC config, Secrets Manager, or connection pooling needed
3. **Lambda fit:** Native IAM integration, no networking overhead
4. **Simplicity:** Two-table design (vpcs as primary, subnets with vpc_id as sort key + GSI)
5. **Low friction:** Minimal infrastructure, fast to deploy

### Data Model (NoSQL)
**VPCs Table:**
- Partition key: `vpc_id` (AWS VPC ID, e.g., vpc-xxx)
- Attributes: `vpc_name`, `cidr_block`, `region`, `created_by`, `created_at`, `status`

**Subnets Table:**
- Partition key: `vpc_id` (AWS VPC ID)
- Sort key: `subnet_id` (AWS Subnet ID)
- Attributes: `subnet_name`, `cidr_block`, `availability_zone`, `created_by`, `created_at`, `status`
- GSI on `subnet_id` for direct subnet lookups

### Setup Notes
- Create two DynamoDB tables with on-demand billing
- Grant Lambda execution role permissions: `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query`, `dynamodb:Scan`, `dynamodb:UpdateItem`, `dynamodb:DeleteItem`
- Lambda code queries VPCs by `vpc_id`, subnets by `vpc_id + subnet_id` or via GSI
- Deletion: Python deletes subnets before deleting parent VPC (no CASCADE DELETE, but Lambda handles it)

### Why Not Alternatives
- **RDS Free Tier:** Will eventually cost money; Aurora Serverless scales to zero
- **DynamoDB:** NoSQL requires different data model; Aurora keeps SQL familiar
- **SQLite + S3:** Concurrency issues with multiple Lambda invocations
