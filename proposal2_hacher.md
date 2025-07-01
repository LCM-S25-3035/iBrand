# Milestone 3 - Research Paper Proposal

## Proposal 2: Confidential Serverless Computing (Hacher)

### 📌 Abstract
Although serverless computing offers compelling cost and deployment simplicity advantages, a significant challenge remains in securely managing sensitive data as it flows through the network of ephemeral function executions in untrusted clouds. While Confidential Virtual Machines (CVMs) offer a promising secure execution environment, their integration with serverless architectures currently faces fundamental limitations in security, performance, and resource efficiency.

We present **Hacher**, a confidential computing system for secure serverless deployments. By employing nested confidential execution and a decoupled guest OS within CVMs, Hacher runs each function in a minimal “trustlet,” significantly improving security by reducing the Trusted Computing Base (TCB). Hacher also uses a data-centric I/O architecture built upon a lightweight LibOS to optimize communication performance and resource efficiency.

### 🚀 Key Contributions
- **Security**: 4.3× smaller TCB
- **Performance**: 15–93% improved end-to-end latency
- **Scalability**: Up to 907× higher function density
- **Efficiency**: Up to 27× lower inter-function communication overhead
- **Latency**: 16.7–30.2× reduction in function chaining delay

### 📅 Year
May 1, 2025

### 🧾 Journal
arXiv (Preprint)

### ✍️ Authors
Patrick Sabanic, Masanori Misono, Teofil Bodea, Julian Pritzi, Michael Hackl, Dimitrios Stavrakakis, Pramod Bhatotia

### 🔗 URL
[https://arxiv.org/abs/2504.21518](https://arxiv.org/abs/2504.21518)

---

_Group 4 | Milestone 3 – Research and Study | Assigned to: Amandeep Singh_
