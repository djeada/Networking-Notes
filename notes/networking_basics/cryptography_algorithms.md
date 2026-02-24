# Notes on Key Management and Cryptography Algorithms

## Key Requirements

### **1. Symmetric Key**
   - **Requirement**: \(n \times (n - 1) / 2\) keys are required.
   - **Reason**: Each pair of nodes needs a unique key.

### **2. Public Key**
   - **Requirement**: \(2 \times n\) keys are required.
   - **Reason**: Each node will have a private and a public key.

## Cryptography Algorithms

### **1. RSA Algorithm**
   - **Description**: RSA is an asymmetric cryptographic algorithm used for secure data transmission.
   - **Image**: An image depicting the RSA example is provided.
     ![Rsa Example](images/media/image9.png)

### **2. Diffie-Hellman Key Exchange**
   - **Description**: The algorithm allows two parties to establish a secret key over an insecure channel.
   - **Formulae**:
     - \(R1 = g^{x} \mod p\)
     - \(R2 = g^{y} \mod q\)
     - **Common Secret Key**: \(g^{xy} \mod p\)

## Conclusion
- Understanding the key requirements and algorithms is crucial for implementing secure communication.
