---
name: database-models
description: Database schema and model definitions for VPCs and Subnets
metadata:
  type: project
---

## Database Models

**Files:**
- `docs/planning-board/database-models.md` — SQL schema definition and design notes
- `src/models.py` — SQLAlchemy ORM models for database interaction
- `src/schema.py` — Pydantic dataclass models for API request/response validation

**Tables:**

1. **VPCs** - Stores AWS VPC resources
   - vpc_id (AWS ID), vpc_name, cidr_block, region, created_by, created_at, status

2. **Subnets** - Stores subnets associated with VPCs
   - subnet_id (AWS ID), vpc_id (FK), subnet_name, cidr_block, availability_zone, created_by, created_at, status

**Key Design:**
- AWS IDs (vpc_id, subnet_id) stored for AWS verification
- Soft deletes via status field
- Audit trail with created_by
- Cascade delete: removing VPC removes its subnets
