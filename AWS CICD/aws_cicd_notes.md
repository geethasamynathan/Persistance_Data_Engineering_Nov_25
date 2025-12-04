
# CI/CD with AWS CodePipeline, CodeBuild, and CodeDeploy  
### Beginner to Advanced Notes for Data Engineering Students  
---

## 1. What is CI/CD?

### CI: Continuous Integration  
Automatically merges and tests code every time a developer pushes changes.

### CD: Continuous Deployment / Delivery  
Automatically deploys the tested code into servers (EC2, Lambda, ECS).

### Simple Definition:  
**CI/CD automates moving code → build → test → deploy without manual steps.**

---

## 2. Why Data Engineers Need CI/CD

Data Engineers frequently modify:

- ETL/ELT Python scripts  
- Airflow DAGs  
- Data APIs  
- Lambda jobs  
- Spark/Glue workflows  

CI/CD ensures:

| Without CI/CD | With CI/CD |
|---------------|------------|
| Manual uploads | Automated deployment |
| Manual testing | Automated testing |
| Human errors | Stable deployments |
| Slow release | Fast delivery |

---

## 3. Old Approach (Before CI/CD)

### Previous workflow:
1. Developer writes code  
2. Zips project manually  
3. Uploads to EC2  
4. SSH into server  
5. Restart server  
6. Debug manually  

### Problems  
- Slow  
- Error-prone  
- Hard to rollback  
- Not scalable  

---

## 4. Modern CI/CD Workflow

```
Local Code → CodeCommit → CodePipeline → CodeBuild → CodeDeploy → EC2 Server
```

**All steps are AUTOMATED.**

---

## 5. AWS Services Used in CI/CD

| AWS Service | Why Used |
|------------|-----------|
| **CodeCommit** | Git repository |
| **CodePipeline** | CI/CD orchestration |
| **CodeBuild** | Build + Run tests |
| **CodeDeploy** | Deploy to EC2 |
| **EC2** | Server for hosting Python app |

---

## 6. Example Project: Deploy Python Flask App With CI/CD

We will deploy:

- A small Flask app  
- Built using CodeBuild  
- Deployed using CodeDeploy  
- Triggered by CodePipeline  

---

## 7. Folder Structure

```
my-python-app/
│
├── app.py
├── requirements.txt
├── buildspec.yml
├── appspec.yml
└── scripts/
      └── start_server.sh
```

---

## 8. Python Application: `app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Data Engineers! CI/CD Deployment Successful 🎉"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 9. Requirements File: `requirements.txt`
```
flask
```

---

## 10. Build Specification: `buildspec.yml`

```yaml
version: 0.2

phases:
  install:
    commands:
      - echo "Installing dependencies..."
      - pip install -r requirements.txt -t .
  build:
    commands:
      - echo "Packaging build files"
artifacts:
  files:
    - '**/*'
```

---

## 11. Deployment Specification: `appspec.yml`

```yaml
version: 0.0
os: linux

files:
  - source: /
    destination: /home/ec2-user/python-app/

hooks:
  AfterInstall:
    - location: scripts/start_server.sh
      timeout: 300
```

---

## 12. Start Script: `scripts/start_server.sh`

```bash
#!/bin/bash
cd /home/ec2-user/python-app
nohup python3 app.py > output.log 2>&1 &
```

Make it executable:
```
chmod +x scripts/start_server.sh
```

---

## 13. EC2 Setup (Required)

Run the following after launching an EC2 instance:

### Install Python & Flask
```bash
sudo yum update -y
sudo yum install python3 -y
pip3 install flask
```

### Create App Directory
```
mkdir /home/ec2-user/python-app
```

### Install CodeDeploy Agent

```bash
sudo yum install ruby -y
sudo yum install wget -y
cd /home/ec2-user
wget https://aws-codedeploy-ap-south-1.s3.ap-south-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo systemctl enable codedeploy-agent
sudo systemctl start codedeploy-agent
```

---

## 14. CI/CD Pipeline Setup Steps

### **Step 1 — CodeCommit**
- Create a repository  
- Push your entire folder structure

### **Step 2 — CodeDeploy**
- Create Application → EC2/On-premise  
- Create Deployment Group → Select your EC2  
- Attach IAM Role: `CodeDeployRole`

### **Step 3 — CodeBuild**
- Runtime: Ubuntu / Standard image  
- Buildspec file: `buildspec.yml`  
- Output artifact: ZIP  

### **Step 4 — CodePipeline**
Pipeline stages:

1. **Source** (CodeCommit)  
2. **Build** (CodeBuild)  
3. **Deploy** (CodeDeploy)  

---

## 15. How to View Deployment

After deployment finishes:

1. Go to EC2 console  
2. Copy the **Public IP**  
3. Open in browser:

```
http://YOUR_PUBLIC_IP:5000
```

You should see:

> **"Hello Data Engineers! CI/CD Deployment Successful 🎉"**

---

## 16. How CI/CD Helps Data Engineering

### CI/CD automates:

- ETL script updates  
- Airflow DAG deployments  
- Lambda jobs  
- API microservices  
- Dependency management  
- Scheduled job deployments  

### Benefits:
- No manual intervention  
- No SSH required  
- Version-controlled deployments  
- Team collaboration  
- Faster releases  

---

## 17. Summary Cheat Sheet

| Term | Meaning |
|------|---------|
| CI/CD | Automates code build → test → deploy |
| CodeCommit | Git repo |
| CodeBuild | Build + Test code |
| CodeDeploy | Deploy code to EC2 |
| CodePipeline | Manages whole workflow |
| EC2 | Server where app runs |

---

## Need More?

Available on request:

- Architecture diagram  
- Airflow CI/CD pipeline example  
- Data engineering ETL CI/CD example  
- Python Lambda CI/CD example  
- Docker + ECS CI/CD  

