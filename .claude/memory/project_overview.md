---
name: project-overview
description: High-level project context and goals
metadata:
  type: project
---

## AWS VPC Assignment API Platform

**Status:** Early stage (initialized with documentation, src/ is empty)

**Objective:** Create a Python REST API that manages AWS VPC and subnet resources programmatically.

**Core Requirements:**
- REST API endpoint for creating VPCs with multiple subnets
- API endpoint for retrieving created resource data
- Authentication layer (API keys or similar)
- Authorization: open to all authenticated users
- Store VPC/subnet metadata somewhere (database TBD)
- Infrastructure automation via Terraform for AWS deployment

**Bonus Goal:** Use AWS serverless services (Lambda, API Gateway, DynamoDB, etc.)

**Deliverable:** Complete codebase and documentation in GitHub repo, with demo/presentation capability

**Key Directories:**
- `docs/planning-board/` - Requirements and problem statement
- `docs/documentation/` - User guides and operator manuals (to be populated)
- `terraform/` - IaC for AWS deployment (empty, to be populated)
- `src/` - Python application code (empty, to be developed)

**Tech Stack (Confirmed):**
- Python (application code)
- AWS Lambda (serverless compute)
- AWS S3 (object storage)
- SQL Database (engine TBD)
- Terraform (infrastructure-as-code)
