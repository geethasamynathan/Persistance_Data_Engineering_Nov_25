# Data Security & Governance in AWS Databricks – Training Notes

## 1. What is Data Security & Governance?
Data Security & Governance ensures that data is:
- Secure  
- Accurate  
- Consistent  
- Compliant  
- Auditable  

It protects data throughout the lifecycle:  
**Ingestion → Storage → Processing → Access → Analytics → Sharing**

## 2. What is Unity Catalog?
Unity Catalog is Databricks’ centralized governance and security layer that manages:
- Data Access  
- Data Lineage  
- Data Discovery  
- Data Classification  
- Data Auditing  
- Table Permissions  
- File Permissions  
- ML Model Governance  

Unity Catalog = One place to manage access and governance for all Databricks data.

## 3. Importance of Unity Catalog
- Standard governance across AWS, Azure, GCP  
- Centralized access control for all workspaces  
- Secure data sharing (Delta Sharing)  
- Column & row-level security  
- Automated end-to-end lineage  
- Compliance (GDPR, HIPAA, RBI, PCI-DSS)  
- Enables least-privilege access model  

## 4. Unity Catalog Components

### 4.1 Metastore
Top-level governance container storing:
- Schemas  
- Tables  
- Permissions  
- Storage locations  

### 4.2 Catalog
Logical grouping of schemas.

### 4.3 Schema
Grouping of tables and views.

### 4.4 Tables
Two types:
- Managed tables  
- External tables (S3-governed)

### 4.5 Storage Credential
IAM role/key that enables secure S3 access.

### 4.6 External Location
Mapping of S3 paths to Unity Catalog.

### 4.7 Data Lineage
Tracks table dependencies, notebook operations, dashboards.

### 4.8 Permissions & RBAC
Supports:
- GRANT SELECT  
- GRANT MODIFY  
- GRANT OWNERSHIP  
- Column masking  
- Row filters  

### 4.9 Delta Sharing
Secure external data sharing without copies.

## 5. How Unity Catalog Works (Step-by-Step)

### Step 1: Create S3 Bucket
```
company-data-lake/
    bronze/
    silver/
    gold/
```

### Step 2: Create IAM Role

### Step 3: Create Unity Metastore

### Step 4: Create Storage Credential
```sql
CREATE STORAGE CREDENTIAL finance_role
WITH IAM_ROLE = 'arn:aws:iam::11111:role/databricks-data-role';
```

### Step 5: Create External Location
```sql
CREATE EXTERNAL LOCATION finance_ext
URL 's3://company-data/finance/'
WITH STORAGE CREDENTIAL finance_role;
```

### Step 6: Create Catalog
```sql
CREATE CATALOG finance_catalog;
```

### Step 7: Create Schema
```sql
CREATE SCHEMA finance_catalog.transactions;
```

### Step 8: Create Table
```sql
CREATE TABLE finance_catalog.transactions.sales
USING DELTA LOCATION 's3://company-data/finance/sales';
```

### Step 9: Apply Permissions
```sql
GRANT SELECT ON TABLE finance_catalog.transactions.sales TO analyst_role;
```

### Step 10: Track Lineage

## 6. Real-World Use Cases
- Banking  
- Retail  
- Healthcare  
- Manufacturing  
- AI/ML Governance  

## 7. Governance Setup
1. Identify domains  
2. Create catalogs  
3. Create schemas  
4. Configure IAM + S3  
5. Create storage credentials  
6. Build tables  
7. Apply RBAC  
8. Build masking  
9. Enable lineage  
10. Enable CloudTrail  

## 8. Enterprise Benefits of Unity Catalog
| Requirement | Benefit |
|------------|---------|
| Security | Column/row-level policies |
| Compliance | GDPR, HIPAA, RBI |
| Scalability | Single governance layer |
| Multi-region | One Metastore per region |
| Lineage | Automatic tracking |
| ML governance | MLflow integration |
| Multi-cloud | Same experience |

