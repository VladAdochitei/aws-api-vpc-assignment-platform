---
name: authorization-decision
description: Chosen authorization approach for the API
metadata:
  type: project
---

## Authorization Approach: Lambda Authorizers with API Keys

**Decision:** Use Lambda Authorizer to validate API keys for all requests.

**Why:** Simplicity, quick setup (~2 hours), minimal cost, no external dependencies, meets MVP timeline.

**Flow:**
1. Client sends `X-API-Key: <key>` header
2. Lambda Authorizer validates key against allowed list
3. Return allow/deny policy
4. Business logic Lambda executes if allowed

**Key Storage:**
- **MVP:** Environment variable (comma-separated list)
- **Production:** DynamoDB or Secrets Manager

**Not chosen:** Cognito (too much overhead for MVP), Full JWT (overkill initially)

**Timeline:** Can be implemented in ~2 hours for initial version
