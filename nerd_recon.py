# ---------------------------------------------------------
# Tool: Nerd Recon v2.0
# Author: [Ilana Belinson :)]
# Purpose: Web Reconnaissance & Vulnerability Analysis
# Created for: Cybersecurity Studies 2026
# ---------------------------------------------------------

import os
import sys
import time

# --- Elegant Color Palette ---
CYAN   = '\033[96m'
PINK   = '\033[95m'
BLUE   = '\033[94m'
YELLOW = '\033[93m'
GREEN  = '\033[92m'
RED    = '\033[91m'
BOLD   = '\033[1m'
END    = '\033[0m'

def show_banner():
    os.system('clear')
    # Minimalist yet unique ASCII Banner
    print(f"{PINK}{BOLD}" + "═"*60)
    print(f"""
    _   _               _   ____                          
   | \ | | ___ _ __  __| | |  _ \ ___  ___ ___  _ __      
   |  \| |/ _ \ '__|/ _` | | |_) / _ \/ __/ _ \| '_ \     
   | |\  |  __/ |  | (_| | |  _ <  __/ (_| (_) | | | |     
   |_| \_|\___|_|   \__,_| |_| \_\___|\___\___/|_| |_|     
                                            (o-o) v2.0
    """)
    print("═"*60 + f"{END}")
    print(f"{BLUE}[*] Initializing Cyber Reconnaissance Suite...{END}")
    print(f"{BLUE}[*] Focus: Efficiency, Clarity, and Results.{END}\n")
    time.sleep(1)

def run_step(step_num, title, command):
    print(f"{YELLOW}{BOLD}[Step {step_num}/3] {title}{END}")
    print(f"{BLUE}Executing:{END} {CYAN}{command}{END}")
    # Running the command
    os.system(command)
    print(f"{GREEN}✔ Done.{END}\n")

def analyze_results(folder):
    print(f"{PINK}{BOLD}" + "█"*20 + " PINK ANALYSIS SUMMARY " + "█"*20 + f"{END}")
    keywords = ["VULNERABLE", "CVE-", "Admin", "Config", "Backup", "Editable", "Password", "CVS", "Direct"]
    found = False
    
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            try:
                with open(f"{folder}/{filename}", 'r') as f:
                    content = f.read()
                    for key in keywords:
                        if key.lower() in content.lower():
                            found = True
                            print(f"{PINK}{BOLD}[!] ALERT:{END} Found '{key}' in {filename}")
            except: continue
                
    if not found:
        print(f"{WHITE}[*] No obvious critical keywords found. Ready for manual review.")
    print(f"{PINK}{BOLD}" + "█"*63 + f"{END}\n")

def main():
    show_banner()
    
    # Clean and clear input
    target = input(f"{BLUE}{BOLD}» Enter Target URL/IP:{END} ").strip()
    if not target: 
        print(f"{RED}Error: No target provided.{END}")
        sys.exit()
    
    # Create a clean folder name
    clean_target = target.replace("http://", "").replace("https://", "").replace("/", "").replace(".", "_")
    folder_name = f"recon_{clean_target}"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # --- Step 1: Technology Fingerprinting ---
    run_step(1, "Technology Fingerprinting (WhatWeb)", 
             f"whatweb -a 3 {target} > {folder_name}/1_fingerprint.txt")

    # --- Step 2: Advanced Network Discovery ---
    nmap_target = target.replace("http://", "").replace("https://", "").split('/')[0]
    run_step(2, "Vulnerability & Service Discovery (Nmap)", 
             f"nmap -F -sV --script vuln,http-enum -T4 {nmap_target} > {folder_name}/2_network_report.txt")

    # --- Step 3: Content Fuzzing ---
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if os.path.exists(wordlist):
        ffuf_url = target if target.startswith("http") else f"http://{target}"
        run_step(3, "Directory & File Fuzzing (FFUF)", 
                 f"ffuf -t 64 -u {ffuf_url}/FUZZ -w {wordlist} -mc 200,301 -o {folder_name}/3_fuzz_report.txt -s")
    else:
        print(f"{RED}[!] Wordlist missing. Skipping FFUF.{END}\n")

    # --- Final Analysis ---
    analyze_results(folder_name)
    
    # --- Final Bold Message ---
    print(f"{GREEN}{BOLD}" + "═"*60)
    print(f" SUCCESS: Reconnaissance mission complete.")
    print(f" All findings are neatly organized in the folder:")
    print(f" > {folder_name} <")
    print(f" Happy hunting! :)")
    print("═"*60 + f"{END}\n")

if __name__ == "__main__":
    main()
