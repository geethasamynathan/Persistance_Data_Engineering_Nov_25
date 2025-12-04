
# AWS CloudTrail for Compliance & Audit Trails

## 🔵 Introduction
AWS CloudTrail is a service that records **all API calls and user activity** across your AWS environment. It is the foundational AWS service for **security, governance, auditing, change tracking, and compliance** with regulations such as SOC2, GDPR, HIPAA, PCI-DSS, ISO 27001, and RBI guidelines.

CloudTrail logs WHO did WHAT, WHEN, WHERE, and HOW in AWS.

In simple terms:  
👉 **CloudTrail = CCTV Camera of AWS**

---

# 🟦 Why CloudTrail Is Critical for Compliance

### CloudTrail ensures:
- Full traceability of all AWS actions  
- Immutable logs for audit & investigations  
- Visibility into unauthorized access  
- Monitoring of sensitive API activities  
- Historical evidence for auditors  

### Required for:
- SOC2 Type-II  
- ISO 27001  
- HIPAA  
- GDPR  
- PCI-DSS  
- RBI financial compliance  
- Any internal InfoSec or governance requirement  

---

# 🟩 Real-World Use Cases

## 1️⃣ Data Engineering Compliance
CloudTrail monitors:
- Who deleted S3 objects  
- Who modified Glue Data Catalog  
- Who triggered Athena or EMR jobs  
- Changes in KMS encryption policies  

**Example audit:**  
“Who deleted the S3 file in the raw zone on Oct 10?”  
CloudTrail gives the answer instantly.

---

## 2️⃣ Security & Incident Response
Track suspicious activities:
- IAM policy changed unexpectedly  
- Security group opened to 0.0.0.0/0  
- Unauthorized KMS decrypt attempts  
- Console login from unknown IP  

---

## 3️⃣ Governance & Configuration Auditing
Identify misconfigurations:
- EC2 instance resized  
- EBS snapshots shared publicly  
- RDS instance deleted  
- Glue job overwritten  

---

## 4️⃣ Forensics & Root Cause Analysis
During security incidents, CloudTrail helps identify:
- Timeline of events  
- Actor behind the change  
- IP address and location  

---

## 5️⃣ Machine Learning & Data Pipelines
Monitor:
- Who triggered SageMaker jobs  
- ETL workflow modifications  
- Glue Development Endpoint access  

---

# 🟦 CloudTrail Log Contents

Sample event:

```json
{
  "eventTime": "2025-12-03T10:23:12Z",
  "eventName": "PutObject",
  "awsRegion": "ap-south-1",
  "sourceIPAddress": "10.0.2.14",
  "userIdentity": {
      "type":"IAMUser",
      "userName":"data_engineer01"
  },
  "requestParameters": {
      "bucketName":"sales-lake",
      "key":"raw/2025/12/03/file.csv"
  }
}
```

Reveals:
- Who: `data_engineer01`  
- What: uploaded a file  
- Where: S3 bucket `sales-lake`  
- When: precise timestamp  
- How: using AWS SDK  

---

# 🟧 Types of CloudTrail Trails

| Type | Description |
|------|-------------|
| **Management Events** | Resource-level actions (EC2, S3, RDS, IAM) |
| **Data Events** | S3 object-level logs & Lambda invoke logs |
| **CloudTrail Insights** | Anomaly detection for security behaviors |

---

# 🟨 Step-by-Step Setup: CloudTrail for Compliance

## **Step 1 — Create a CloudTrail Trail**
1. Go to CloudTrail console  
2. Click **Create Trail**  
3. Trail name: `org-compliance-trail`  
4. Enable **Apply trail to all Regions**  
5. Choose S3 bucket  
6. Enable **Log file integrity validation**  

---

## **Step 2 — Enable Data Events**
Track S3 object-level activity:

- `PutObject`  
- `GetObject`  
- `DeleteObject`  

Also track Lambda `Invoke` events.

---

## **Step 3 — Enable CloudTrail Insights**
Detect anomalies:
- IAM privilege escalation  
- Unusual API usage  
- Unexpected service calls  

---

## **Step 4 — Query Logs with Athena**
Create Athena table:

```sql
CREATE EXTERNAL TABLE cloudtrail_logs (
    eventTime string,
    eventName string,
    userIdentity struct<userName:string>,
    sourceIPAddress string,
    awsRegion string,
    requestParameters string
)
PARTITIONED BY (region string, year string, month string, day string)
LOCATION 's3://cloudtrail-logs/AWSLogs/';
```

### Example Audit Query:
```
SELECT eventTime, userIdentity.userName, eventName
FROM cloudtrail_logs
WHERE eventName = 'DeleteObject'
AND eventTime LIKE '2025-12-03%';
```

---

## **Step 5 — Send Alerts (CloudWatch + SNS)**
Example metric filter for failed logins:

```
$.eventName = "ConsoleLogin" && $.errorMessage = "Failed authentication"
```

Alerts sent to:
- Email  
- Slack  
- PagerDuty  

---

# 🟦 Best Practices for Compliance

| Best Practice | Reason |
|---------------|--------|
| Enable Org-level trail | Centralized auditing |
| Store logs in a separate security account | Prevent tampering |
| Enable S3 Object Lock | Immutable audit logs |
| Enable Insights | Detect anomalies |
| Use Athena for querying logs | Fast investigations |
| Forward logs to SIEM | Enterprise monitoring |
| Track CloudTrail via AWS Config | Governance |

---

# ⭐ Summary (Simple)
- AWS CloudTrail logs **every AWS API call** for accountability and compliance.  
- Critical for **security, governance, audits, and incident response**.  
- Integrates with **S3, CloudWatch, Athena, KMS, SIEM, Data Engineering tools**.  
- CloudTrail is mandatory for enterprise compliance frameworks.

Generated for **ItTechGenie** 🚀
