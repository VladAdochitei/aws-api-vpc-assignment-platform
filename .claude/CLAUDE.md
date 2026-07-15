# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS VPC Assignment API Platform - A Python API service for programmatically creating and managing AWS VPC resources with multiple subnets. The API includes authentication, persistence, and infrastructure-as-code (Terraform) for deployment.

**Key Requirements:**
- REST API in Python for VPC/subnet creation and retrieval
- Authentication layer (all authenticated users authorized)
- AWS integration for resource creation
- Store and retrieve created resource data
- Infrastructure automation via Terraform

## Development Approach

- **Simplicity over efficiency:** Write clear, maintainable code that's easy to recall and modify. Prefer straightforward solutions over clever optimizations.
- **Incremental evolution:** Guide feature development step-by-step. Do not design speculatively for future needs.
- **Python stack:** All backend systems use Python.

## Repository Structure

```
.claude/          - Claude Code configuration
docs/             - Planning and documentation
  planning-board/ - Problem statement and requirements
  documentation/  - User guides and operator manuals
src/              - Python application code (TBD)
terraform/        - Infrastructure-as-code for AWS deployment
```

## Development Commands

*(To be established once project structure is defined)*

When setting up the project:
- Linting: `pytest --linter` or equivalent
- Tests: `pytest` or `pytest tests/test_module.py` for single test file
- API server: `python -m app.main` or similar (command TBD)
- Format: Black or similar code formatter (TBD)

## Technology Stack

- **Compute:** AWS Lambda (serverless functions)
- **API Gateway:** AWS API Gateway (triggers Lambda)
- **Storage:** S3 (object/file storage)
- **Database:** SQL database (engine TBD)
- **IaC:** Terraform

## Architecture (TBD)

As the project develops, document here:
- Lambda function organization and handlers
- API endpoints and request/response schemas
- Authentication mechanism (e.g., API keys, JWT)
- Database schema for VPC resource metadata
- AWS service interactions (EC2, VPC APIs)
- S3 usage patterns
- Terraform module organization

## Notes for Future Work

- Keep database schema simple and explicit
- Make API endpoints straightforward and predictable
- Document authentication flow clearly
- Terraform should be modular and easy to understand
