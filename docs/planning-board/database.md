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

## Decision: Aurora Serverless v2

**CHOSEN APPROACH** for this project:
- PostgreSQL-compatible Aurora Serverless v2
- Scales automatically based on demand
- Costs pennies during PoC phase (scales to zero when idle)
- SQL capabilities match project requirements

### Why Aurora Serverless v2
1. **Cost:** Absolutely minimal for PoC usage
2. **Familiarity:** Standard SQL, similar to traditional RDS
3. **Serverless:** Works well with Lambda-based API architecture
4. **No capacity planning:** Auto-scales, no need to right-size instances
5. **Production-ready:** When scaling up, infrastructure is already there

### Setup Notes
- Create a serverless v2 Aurora cluster
- Store connection credentials in Secrets Manager
- Lambda functions retrieve secrets and connect
- Database can be accessed from Lambda VPC or via RDS proxy

### Why Not Alternatives
- **RDS Free Tier:** Will eventually cost money; Aurora Serverless scales to zero
- **DynamoDB:** NoSQL requires different data model; Aurora keeps SQL familiar
- **SQLite + S3:** Concurrency issues with multiple Lambda invocations
