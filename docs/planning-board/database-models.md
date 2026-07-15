# Database Models

## SQL Schema

### VPC Table
```sql
CREATE TABLE vpcs (
  id SERIAL PRIMARY KEY,
  vpc_id VARCHAR(255) UNIQUE NOT NULL,      -- AWS VPC ID (vpc-xxx)
  vpc_name VARCHAR(255) NOT NULL,            -- User-friendly name
  cidr_block VARCHAR(18) NOT NULL,           -- e.g., 10.0.0.0/16
  region VARCHAR(50) NOT NULL,               -- AWS region (eu-west-1)
  created_by VARCHAR(255),                   -- API key or user who created it
  created_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active'        -- active, pending, deleted
);
```

### Subnet Table
```sql
CREATE TABLE subnets (
  id SERIAL PRIMARY KEY,
  subnet_id VARCHAR(255) UNIQUE NOT NULL,    -- AWS subnet ID (subnet-xxx)
  vpc_id VARCHAR(255) NOT NULL,              -- Foreign key to vpcs table
  subnet_name VARCHAR(255) NOT NULL,
  cidr_block VARCHAR(18) NOT NULL,           -- e.g., 10.0.1.0/24
  availability_zone VARCHAR(50),             -- e.g., eu-west-1a
  created_by VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active',
  FOREIGN KEY (vpc_id) REFERENCES vpcs(vpc_id) ON DELETE CASCADE
);
```

## Design Notes

- **AWS IDs:** `vpc_id` and `subnet_id` store actual AWS resource IDs for verification
- **Soft deletes:** `status` field allows marking as deleted without removing data
- **Audit trail:** `created_by` tracks who created each resource
- **Relationships:** Subnets reference VPCs via foreign key with cascade delete
- **Timestamps:** All records track creation time

## Common Queries

- Get all VPCs for a user: `SELECT * FROM vpcs WHERE created_by = ? AND status = 'active'`
- Get subnets for a VPC: `SELECT * FROM subnets WHERE vpc_id = ? AND status = 'active'`
- Verify resource exists: `SELECT * FROM vpcs WHERE vpc_id = ?`
- Get all resources (including deleted): `SELECT * FROM vpcs WHERE created_by = ?`
