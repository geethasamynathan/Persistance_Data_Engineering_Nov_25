
# AWS KMS (Key Management Service) – Complete Notes

## 🔐 What is AWS KMS?
AWS Key Management Service (KMS) is a fully managed service that allows you to create, store, manage, rotate, and control cryptographic keys used to encrypt your data across AWS.

---

## 🎯 Why Use AWS KMS?
- Protect sensitive data (PII, financial, healthcare)
- Centralized key management
- AWS‑native encryption for S3, Glue, EMR, Redshift, MSK, Lambda, Athena
- Fine‑grained key access control via IAM + Key Policies
- Compliance (HIPAA, PCI-DSS, GDPR)
- Full audit logging via CloudTrail

---

## 🌍 Real‑World Use Cases
### 1. Encrypt Data in S3 Buckets  
Using SSE‑KMS ensures that all sensitive objects (PAN, Aadhaar, customer files) remain encrypted.

### 2. Encrypt Data Engineering Pipelines  
Used with Glue, EMR, Databricks, Kinesis, EventBridge, Lambda.

### 3. Store Secrets Securely  
Secrets Manager + KMS protects:
- DB credentials  
- API keys  
- OpenAI keys  
- OAuth tokens  

### 4. Client‑Side Encryption (Envelope Encryption)  
FinTechs encrypt data **before** sending to AWS.

### 5. Encrypt Redshift, RDS, MSK, DynamoDB  
KMS integrates with almost all AWS data‑layer services.

---

## 🧱 Types of Keys in KMS
| Type | Description | Usage |
|------|-------------|--------|
| AWS‑Managed Keys | Auto‑created by AWS | `aws/s3`, `aws/rds` |
| Customer‑Managed Keys (CMK) | You create + control | Full access control |
| Symmetric Keys | Most common | S3, Glue, EMR |
| Asymmetric Keys | RSA/ECC | Digital signatures |

---

## 🪜 Step‑by‑Step Guide: Using AWS KMS

### **Step 1 — Create a CMK**
1. Go to **AWS Console → KMS**
2. Click **Create key**
3. Choose **Symmetric**
4. Set alias → `alias/data-pipeline-key`
5. Add administrators + key‑users
6. Finish

---

### **Step 2 — Add IAM Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:ap-south-1:123456789012:key/<key-id>"
    }
  ]
}
```

---

### **Step 3 — Enable Encryption on S3**
Go to bucket → **Properties → Default Encryption**  
Select:
- `SSE-KMS`
- Choose your CMK

---

## 🔵 Integrating KMS with Data Engineering Tools

---

### **1. AWS Glue**
Enable encryption for:
- Scripts
- Temp directory
- Job bookmarks
- Output data

Glue Spark example:
```python
df.write   .option("aws:kmsKeyId", "alias/data-pipeline-key")   .mode("overwrite")   .save("s3://my/output/")
```

---

### **2. AWS EMR (Spark)**
Cluster creation:
```
--encryption-type KMS --kms-key-id alias/data-pipeline-key
```

---

### **3. Databricks on AWS**
```python
df.write   .option("fs.s3.enableKmsEncryption", "true")   .option("fs.s3.kms.keyId", "alias/data-pipeline-key")   .parquet("s3://datalake/bronze/")
```

---

### **4. Athena**
Configure:
- Query result location → S3  
- Encryption → SSE‑KMS  

---

### **5. Secrets Manager**
Retrieve secret:
```python
import boto3
client = boto3.client('secretsmanager')

secret = client.get_secret_value(SecretId="openai/credentials")
print(secret["SecretString"])
```

---

### **6. Lambda**
Decrypt inside function:
```python
kms.decrypt(CiphertextBlob=data)["Plaintext"]
```

---

### **7. Redshift**
Redshift uses KMS to encrypt:
- Data blocks
- Snapshots
- Temporary data

---

## 🧩 Envelope Encryption (How KMS Works Internally)
1. KMS generates **Data Encryption Key (DEK)**  
2. Application encrypts data using DEK  
3. DEK itself is encrypted using CMK  
4. Store encrypted DEK + ciphertext together  

This is highly scalable for large ETL pipelines.

---

## 🛑 What Happens If You Don't Use KMS?
- Data stored unencrypted  
- Fails audits (GDPR, HIPAA, PCI)  
- Secrets exposed in plaintext  
- No rotation or centralized key control  
- High security risk  

---

## ⭐ Final Summary
AWS KMS is essential for:
- Data Engineering pipelines  
- Securing S3 + ETL outputs  
- Glue/EMR/Athena/Databricks integration  
- Secrets Manager protection  
- Cloud compliance  

It is the **backbone of encryption across AWS**.

---

Generated for ItTechGenie 🚀
