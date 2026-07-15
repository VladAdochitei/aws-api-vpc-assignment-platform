---
name: tech-stack-decisions
description: Confirmed technology choices for the platform
metadata:
  type: project
---

## Confirmed Technology Stack

- **Language:** Python
- **Compute:** AWS Lambda (serverless functions)
- **Storage:** S3 (object storage)
- **Database:** SQL database (choice of specific engine TBD - PostgreSQL, MySQL, etc.)

**Why:** Leverages AWS serverless to keep infrastructure simple and scalable.

**Implication:** API Gateway will likely trigger Lambda functions, which will interact with the SQL database and S3 as needed.
