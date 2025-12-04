
# Access Control Lists (ACLs) & RBAC in AWS – Detailed Notes

## 1. Introduction
AWS provides multiple mechanisms to control who can access resources and how they interact with them. Two major models are:

- **Access Control Lists (ACLs)**
- **Role-Based Access Control (RBAC)** via IAM

---

## 2. Access Control Lists (ACLs)

ACLs are low-level, rule-based permission systems applied directly on resources.

### Types of ACLs in AWS
1. **S3 ACLs**
2. **VPC Network ACLs (NACLs)**

---

## 2.1 S3 Bucket ACLs
S3 ACLs provide object-level and bucket-level permissions. They are a legacy feature and not the recommended method today.

### Permissions Available
- READ  
- WRITE  
- READ_ACP  
- WRITE_ACP  
- FULL_CONTROL  

### Used To Grant Permissions To:
- Other AWS accounts  
- Predefined S3 groups (e.g., AllUsers)

### Example Use Case
Public read access for specific media files stored in S3.

### Limitations
- Hard to maintain  
- Limited conditions  
- Not scalable for enterprise environments  

---

## 2.2 Network ACLs (NACLs)
NACLs are subnet-level firewalls inside VPCs.

### Key Characteristics
- **Stateless**: Inbound and outbound rules are evaluated separately.
- **Ordered Rules**: Rules evaluated from lowest to highest number.
- **Default NACL**: Allows all traffic.
- **Custom NACL**: Denies all until rules added.

### Example Rule
| Rule # | Type | Protocol | Port | Source | Action |
|--------|------|----------|------|--------|--------|
| 100 | Inbound | TCP | 80 | 0.0.0.0/0 | ALLOW |
| 200 | Inbound | ALL | ALL | 0.0.0.0/0 | DENY |

### Use Cases
- Adding extra security to public-facing subnets  
- Blocking suspicious IP ranges  
- Enforcing network-level isolation  

---

## 3. Role-Based Access Control (RBAC) in AWS

AWS implements RBAC through:
- IAM Users  
- IAM Groups  
- IAM Roles  
- IAM Policies  
- AWS Organizations (SCPs)

---

## 3.1 IAM Users
Represents an individual who needs access to AWS.

### Authentication Methods:
- Console password  
- Access keys  

---

## 3.2 IAM Groups
A group of IAM users.

### Purpose:
Assign common permissions (via policies) to multiple users at once.

---

## 3.3 IAM Roles
Roles define permissions and are assumed by:
- AWS services  
- IAM users  
- External identity providers  
- Applications  

### Key Features:
- No long-term credentials  
- Temporary STS-based access  
- Ideal for cross-service communication  

### Example Roles
- `EC2-S3ReadOnly`  
- `Lambda-DynamoDBWrite`  
- `AdminRole`  
- `Billing-ReadOnly`  

---

## 3.4 IAM Policies
IAM policies define allowed or denied actions on resources.

### Sample RBAC Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

---

## 4. ACL vs RBAC – Comparison

| Feature | ACL | RBAC (IAM) |
|--------|-----|------------|
| Scope | Object or subnet level | Uses users, groups, roles |
| Complexity | Simple, rule-based | Policy-driven, flexible |
| Recommended | Limited use | Full enterprise use |
| Controls | Traffic & object permissions | All AWS services |
| Granularity | Coarse | Fine-grained |

---

## 5. When to Use ACLs vs RBAC

### Use ACLs When:
- You need public access to specific S3 objects.  
- Subnet traffic filtering is required (via NACLs).  
- You need to block an IP range at subnet level.  

### Use RBAC When:
- Managing user/service permissions.  
- Implementing least privilege.  
- Assigning temporary access.  
- Federating enterprise identities (Azure AD, Okta).  

---

## 6. Real-World Scenarios

### 6.1 RBAC – Developer Access
Developers need access only to Lambda and DynamoDB.  
Solution: Create a group `Developers` and attach relevant policies.

### 6.2 ACL – Public Website Images
Make certain S3 objects publicly available using object ACLs.

### 6.3 NACL – Block Malicious Traffic
Add a DENY rule for a suspicious IP range such as `200.100.50.0/24`.

---

## 7. Best Practices

### ACL Best Practices
- Avoid S3 ACLs unless necessary.  
- Use IAM policies instead.  
- Keep NACL rules simple to reduce evaluation overhead.  

### RBAC Best Practices
- Use IAM roles — avoid long-term access keys.  
- Enable MFA for admin roles.  
- Apply least-privilege principles.  
- Use AWS Organizations SCPs for enterprise-level control.  

---

## 8. Summary

| Component | Purpose |
|----------|---------|
| **ACLs** | Resource-level permissions (S3 objects, subnet traffic) |
| **NACLs** | Subnet-level stateless firewall |
| **RBAC (IAM)** | Full identity and access management |
| **IAM Roles** | Temporary permissions for services & users |
| **IAM Policies** | JSON-based permission definitions |

---

## End of Notes
