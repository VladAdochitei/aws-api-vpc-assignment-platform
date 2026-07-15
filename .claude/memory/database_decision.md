---
name: database-decision
description: Chosen database approach for the API
metadata:
  type: project
---

## Database Choice: Aurora Serverless v2

**Decision:** Use Aurora Serverless v2 (PostgreSQL-compatible) for data persistence.

**Why:** 
- Scales to zero when idle (nearly free during PoC)
- SQL-capable (matches project needs)
- Serverless (works with Lambda architecture)
- No capacity planning needed
- Production-ready when scaling up

**Setup:**
- Aurora Serverless v2 cluster
- Store connection creds in Secrets Manager
- Lambda functions retrieve secrets to connect
- Database auto-scales on demand

**Cost:** Pennies for PoC usage, scales linearly with production traffic

**Alternatives considered:** RDS free tier (costs money when idle), DynamoDB (NoSQL), SQLite+S3 (concurrency issues)
