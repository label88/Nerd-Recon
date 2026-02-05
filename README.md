# NerdRecon Suite v3.0

A high-speed, stealthy reconnaissance tool designed for automated target mapping and vulnerability discovery. 

## Features
- **Funnel Strategy:** Moves from lightweight fingerprinting to deep content discovery.
- **Stealth Mode:** Uses passive version mapping (via `vulners`) to avoid triggering AV/EDR.
- **Noise Reduction:** Automatically separates technical logs from actionable reports.
- **Smart Fuzzing:** Discovers hidden backups (`.bak`, `.zip`) and sensitive directories.

## Real-World Findings (Test Run)
During a scan on `testphp.vulnweb.com`, the tool successfully identified:
- **Server:** Nginx 1.19.0 (Potential CVE-2021-23017).
- **Sensitive Files:** Exposed `index.bak` and `index.zip` archive.
- **Development Leaks:** CVS metadata directories (`/CVS/Entries`).
- **Hidden Paths:** `/admin` and `/secured` entry points.

## Usage
```bash
python3 nerd_recon.py
