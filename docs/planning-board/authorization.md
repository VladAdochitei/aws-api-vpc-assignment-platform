# Authorization Strategy

## Requirement
Authorization should be open to all authenticated users.

## AWS API Gateway Authorization Options

### 1. Lambda Authorizers (Custom Authorizers)
- Write a custom Lambda function that validates requests
- Returns an authorization policy allowing/denying access
- **Pros:** Full control, can implement any validation logic
- **Cons:** Need to maintain custom code
- **Use case:** When you need custom token validation or complex authorization rules

### 2. Amazon Cognito
- Managed user authentication and authorization service
- API Gateway validates JWT tokens from Cognito User Pools
- **Pros:** Managed service, handles user signup/login, token generation
- **Cons:** Additional AWS service to manage
- **Use case:** When you want managed user pools with standard OAuth/OpenID Connect flows

### 3. AWS IAM
- For AWS service-to-service authorization
- **Pros:** Native AWS integration
- **Cons:** Not ideal for general user authentication
- **Use case:** When callers are AWS services/roles, not end users

### 4. API Keys
- Simple key-based validation
- **Pros:** Easy to implement
- **Cons:** Not true authorization, mainly for rate limiting
- **Use case:** Basic API protection, not recommended as sole auth

### 5. Mutual TLS
- Client certificate validation
- **Pros:** Strong security for specific use cases
- **Cons:** Complex certificate management
- **Use case:** B2B or highly secure integrations

## Decision: Lambda Authorizers with API Key Validation

**CHOSEN APPROACH** for this project:
- Lambda Authorizer validates API keys from request headers
- Clients submit `X-API-Key: <key>` header with each request
- Authorizer checks if key is in allowed list
- Return allow/deny policy

### Why This Approach
- **Simplicity:** Straightforward key validation logic
- **Setup time:** ~2 hours to implement
- **Cost:** Negligible (single small Lambda)
- **No external dependencies:** No Cognito, no JWT complexity
- **Quick to production:** MVP in hours

### Implementation Flow
1. Client calls API Gateway endpoint with `X-API-Key` header
2. API Gateway invokes Lambda Authorizer
3. Authorizer validates the key (check against allowed list)
4. If valid: return allow policy → business logic Lambda executes
5. If invalid: return deny policy → request rejected

### Key Storage (MVP → Production)
- **MVP:** Environment variable with comma-separated list
- **Production:** DynamoDB table or AWS Secrets Manager (minimal setup)

### Why Not Alternatives
- **Cognito:** Adds unnecessary complexity (user pools, signup UI) for MVP
- **Full JWT:** Overkill for initial release, upgrade later if needed
- **API Keys alone:** Would require API Gateway throttling workaround; Lambda Authorizer approach is cleaner

## Implementation Notes
- Authorization Lambda should validate credentials quickly (called on every request)
- Store allowed keys in environment variables or database
- API Gateway caches authorization decisions (~300 seconds default)
