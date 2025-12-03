
# AWS Systems Manager (SSM) – Beginner to Advanced Guide

## 1. What is AWS Systems Manager?

AWS Systems Manager (SSM) is an operations and management service used to manage EC2, on‑prem servers, VMs, and hybrid machines through a single unified console.

### Key Features
- Remote command execution
- Secure server access without SSH
- Store/Retrieve secure parameters
- Patch automation
- Operational insights
- Workflow automation
- Hybrid management

---

## 2. Why Use AWS Systems Manager?

| Benefit | Description |
|--------|------------|
| No SSH needed | Access EC2 using Session Manager (browser-based shell) |
| Centralized management | Manage all servers in one place |
| Patch automation | Auto-update Linux/Windows machines |
| Secure secret storage | Parameter Store for configs + secrets |
| Automation | Replace manual tasks with automated workflows |
| Compliance | Track configuration, patch level, and violations |

---

## 3. SSM vs Secrets Manager

| Feature | Systems Manager (Parameter Store) | Secrets Manager |
|--------|----------------------------------|----------------|
| Purpose | Config + basic secrets | Secure secrets + rotation |
| Rotation | No auto-rotation | Built-in rotation (RDS, Aurora) |
| Cost | Free (Standard params) | Paid (~$0.40/secret/month) |
| Data size | 4 KB / 8 KB | Up to 64 KB |
| Encryption | Optional KMS | Always KMS-encrypted |
| Use Cases | Configs, API URLs, simple secrets | DB passwords, OAuth keys |

---

## 4. How SSM Works (Architecture Overview)

- **SSM Agent** runs on EC2/on-prem servers.
- **SSM Service** sends instructions.
- **IAM Role** allows EC2 to communicate with SSM.
- **Users** interact through AWS Console/CLI.

---

## 5. Key Components of Systems Manager

### 5.1 Parameter Store
Used to store:
- Passwords
- DB connection strings
- API keys

Retrieve using CLI:

```
aws ssm get-parameter --name "/prod/db/password" --with-decryption
```

Retrieve using Python:

```python
import boto3
ssm = boto3.client('ssm')
value = ssm.get_parameter(Name="/prod/db/password", WithDecryption=True)
print(value['Parameter']['Value'])
```

---

### 5.2 Session Manager (SSH without SSH)

Allows access to EC2 **without**:
- Key pair  
- Port 22  
- Bastion host  

Steps:
1. Ensure SSM agent installed
2. Attach IAM role → `AmazonSSMManagedInstanceCore`
3. EC2 → Connect → Session Manager

---

### 5.3 Run Command

Run scripts on 1 or 1000 servers at once.

Example:

```
aws ssm send-command   --document-name "AWS-RunShellScript"   --targets Key=tag:Env,Values=Prod   --parameters commands=["yum update -y"]
```

---

### 5.4 Automation Runbooks

Automate tasks such as:
- Stop/start EC2
- Create AMI
- Rotate logs
- Patch systems

---

### 5.5 Patch Manager

Automates OS patching on:
- Windows
- Linux
- On-prem

Steps:
1. Create Patch Baseline  
2. Tag instances with `Patch Group`  
3. Create Maintenance Window  

---

### 5.6 Inventory Management

Collects:
- Installed software
- Network config
- OS details
- Running services

---

## 6. Real‑World Example

### Scenario
A company manages 100 EC2 servers and wants:
- No SSH ports
- Secret storage
- Automated monthly patching

### Solution
1. Attach SSM role to EC2  
2. Block SSH  
3. Use Session Manager for secure access  
4. Store secrets in Parameter Store  
5. Auto patch using Patch Manager  
6. Use Automation runbook to take AMI backup monthly  

---

## 7. Beginner → Advanced Steps

### 🔰 Beginner
- Launch EC2
- Attach SSM role  
- Open Session Manager  

### 🔰 Intermediate
- Create Parameter Store secrets  
- Use Run Command  
- Use State Manager  

### 🔰 Advanced
- Create Automation runbooks  
- Use hybrid activation for on‑prem servers  
- Configure compliance  
- Schedule patching  

---

## 8. Summary

| Component | Purpose |
|----------|----------|
| Parameter Store | Config + secret storage |
| Session Manager | SSH-less secure access |
| Run Command | Execute scripts remotely |
| Patch Manager | Auto patching |
| Automation | Workflow execution |
| Inventory | Collect configuration |
| State Manager | Enforce desired state |

---

## 9🟪 9. When to Use Systems Manager

Use SSM whenever you need:

- ✔ Secure server access
- ✔ No SSH ports
- ✔ Central config management
- ✔ Secret storage
- ✔ Automation workflow
- ✔ Patch management
- ✔ Hybrid cloud management

### 🟥 10. When to Use Secrets Manager Instead

Use AWS Secrets Manager when you need:

- ✔ Automatic password rotation
- ✔ RDS/Aurora secret rotation
- ✔ High-security, auditing-heavy secrets
- ✔ Secrets > 4 KB 

---

