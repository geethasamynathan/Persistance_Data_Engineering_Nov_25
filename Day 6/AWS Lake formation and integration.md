# AWS Lake Formation Integration with Databricks

## 1. Introduction
AWS Lake Formation is a governance, security, and access control layer built on top of Amazon S3 that provides fine‑grained control for tables, columns, and rows.

## 2. Why It's Needed
- S3 permissions are coarse (bucket/object level)
- No centralized governance
- No SQL-level permissions before LF
- Difficulty managing multi-team access

## 3. What Lake Formation Is
A centralized security framework for:
- Table-level permissions
- Column-level masking
- Row-level filtering
- Cross-account sharing
- Tag-based access

## 4. How Databricks Integrates
Databricks cluster IAM role is governed by Lake Formation policies:
Databricks → IAM Role → Lake Formation → S3 Data

## 5. Setup Steps (Beginner)
### Step 1 — Enable Lake Formation
Register S3 path: `s3://mycompany-datalake/`

### Step 2 — Assign Admin Roles
Add Databricks IAM role as Lake Formation administrator.

### Step 3 — Create Databases
Create Glue databases: `bronze_db`, `silver_db`, `gold_db`.

### Step 4 — Grant Permissions
Grant SELECT, INSERT, DESCRIBE, ALTER to the Databricks IAM role.

### Step 5 — Attach IAM Role to Databricks Cluster
Use Instance Profile and restart cluster.

### Step 6 — Verify Access
```python
df = spark.read.table("bronze_db.sales")
display(df)
```

## 6. Intermediate — Governance Examples
### Column-Level Security
Allow only specific columns for certain users.

### Row-Level Security
Apply filters like:
```
customer_state = 'Maharashtra'
```

### Databricks Delta Integration
Register Delta paths inside Glue and allow LF to control access.

## 7. Advanced Integration
### Tag-Based Access Control (TBAC)
Add metadata tags like `pii=true`, enforce policies automatically.

### Cross-Account Sharing
Lake Formation → AWS RAM → Databricks consumer account.

### Unity Catalog + Lake Formation
Use UC as primary governance with LF rules synchronized.

## 8. Real-World Architecture
Databricks → LF → Glue Catalog → S3 lake (Bronze/Silver/Gold)

## 9. Summary
Lake Formation adds:
- Central governance
- Fine-grained security
- Cross-account sharing
- Consistent access control for Databricks workloads
