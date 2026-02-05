# Nerd-Recon v2.0 🤓
**Automated Web Reconnaissance & Vulnerability Analysis Suite**

Nerd-Recon is a precision-engineered tool designed to streamline the reconnaissance phase by automating information gathering and vulnerability discovery.

## 🔍 Key Features
* **Technology Fingerprinting:** Identifies web stacks using **WhatWeb**.
* **Network & Vuln Discovery:** Automated **Nmap NSE** scans for known CVEs and misconfigurations.
* **Content Fuzzing:** Rapid directory and file discovery with **FFUF**.
* **Pink Analysis Engine:** A custom post-scan parser that highlights critical alerts (Vulnerabilities, Admin panels, Config files) for immediate review.

## 💡 Design Philosophy & Tool Selection
This suite follows a "less is more" approach, prioritizing accuracy and actionable intelligence:
* **FFUF over Gobuster**: Chosen for superior speed and multi-threading efficiency.
* **Nmap NSE over Nikto**: Prioritizes verified vulnerability scripts to minimize False Positives.
* **Lightweight & Modular**: Designed to perform the "heavy lifting" of recon before moving to manual analysis in tools like **Burp Suite**.

## 🛠 Usage
```bash
python3 nerd_recon.py
