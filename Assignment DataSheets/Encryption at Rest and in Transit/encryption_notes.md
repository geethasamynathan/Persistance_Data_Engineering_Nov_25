# Encryption at Rest & In Transit – Detailed Notes

## 1. What is Encryption?
Encryption converts readable data (**plaintext**) into unreadable form (**ciphertext**) using cryptographic keys so only authorized users can access it.

### Why Encryption Matters
- **Data Privacy** – Protects sensitive information.
- **Data Security** – Prevents breaches and tampering.
- **Compliance** – Required by standards like HIPAA, GDPR, PCI-DSS.
- **Trust** – Builds customer confidence.

---

## 2. Types of Encryption

### A. Symmetric Encryption
- Uses **one key** for encryption and decryption.
- Fast and ideal for large data.
- Example: AES-256.

**Process:**
```
Plaintext + Symmetric Key → Ciphertext  
Ciphertext + Same Key → Plaintext
```

### B. Asymmetric Encryption
- Uses two keys: **Public Key** (encrypt), **Private Key** (decrypt).
- Example: RSA.

**Process:**
```
Sender encrypts using Public Key  
Recipient decrypts using Private Key
```

---

## 3. Encryption at Rest
Protects stored data on physical media (disks, backups, cloud storage).

### AWS Services Supporting Encryption at Rest

#### A. AWS Key Management Service (KMS)
- Generates, stores, rotates, and manages keys.
- Backed by Hardware Security Modules (HSMs).
- Supports: symmetric, asymmetric, and HMAC keys.

#### B. Amazon EBS
- EC2 disk storage.
- Automatically supports encryption and decryption during read/write.

#### C. Amazon S3
Supports:
- SSE-KMS  
- SSE-S3  
- SSE-C  
- Client-side encryption  

---

## 4. Encryption in Transit
Protects data when traveling between systems or services.

### Why It Is Needed
- Prevents eavesdropping  
- Prevents man-in-the-middle attacks  
- Ensures message integrity  

### Common Protocols
- HTTPS (TLS/SSL)  
- VPN (IPSec)  
- SSH  

---

## 5. AWS Services for Encryption in Transit

### A. CloudFront
- Delivers encrypted content over HTTPS.
- Supports custom SSL certificates.
- Uses ACM for certificate management.

### B. VPC Endpoints
Enable private communication WITHOUT internet exposure.
- **Interface Endpoints**
- **Gateway Endpoints**

### C. VPN Connections
Hybrid secure communication between On-premises and AWS.
- Uses IPSec.

---

## 6. AWS KMS (Key Management Service)

### Key Features
- Central key management.
- Key rotation.
- Key policies to control access.
- Stores keys inside HSM.
- Supports symmetric, asymmetric, and HMAC keys.

### HMAC Overview
Used for:
- Message integrity  
- Authentication  
- Password hashing  
- Digital signatures  

Algorithms:
- HMAC-SHA1  
- HMAC-SHA256  
- HMAC-SHA512  

---

## 7. Encryption Best Practices

### A. Key Management
- Use strong random keys.
- Rotate keys regularly.
- Store keys in secure modules.
- Restrict access using policies.

### B. Encryption Algorithms
Use strong:
- AES-256  
- RSA (large keys)  

Avoid weak:
- DES  
- MD5  

### C. Data Classification
- Identify sensitivity level.
- Encrypt high-priority data first.
- Apply retention policies.

### D. Implementation Practices
- Enable encryption at rest and in transit.
- Use TLS 1.2+.
- Perform audits and patching.
- Maintain compliance documentation.

---

## 8. Summary Table

| Topic | Key Insights |
|-------|--------------|
| Encryption at Rest | Protects stored data (EBS, S3). |
| Encryption in Transit | Protects moving data (HTTPS, VPN). |
| AWS KMS | Manages keys, rotates keys, enforces access control. |
| VPC Endpoints/VPN | Secure communication without public exposure. |
| Best Practices | Strong algorithms, key rotation, data classification. |

---

## End of Notes
