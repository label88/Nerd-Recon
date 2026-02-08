import os
import sys
import time

TURQUOISE = '\033[96m' 
PINK      = '\033[95m'
YELLOW    = '\033[93m'
GREEN     = '\033[92m'
RED       = '\033[91m'
BOLD      = '\033[1m'
END       = '\033[0m'

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{PINK}{BOLD}" + "═"*60)
    print(f"""
    _   _               _   ____                          
   | \ | | ___ _ __  __| | |  _ \                        
   |  \| |/ _ \ '__|/ _` | | |_) / _ \/ __/ _ \| '_ \     
   | |\  |  __/ |  | (_| | |  _ <  __/ (_| (_) | | | |     
   |_| \_|\___|_|   \__,_| |_| \_\___|\___\___/|_| |_|     
                                             (o-o) v3.0
    """)
    print("═"*60 + f"{END}")
    print(f"{TURQUOISE}[*] High-Speed Recon Suite: Funnel Strategy Enabled.{END}")
    print(f"{TURQUOISE}[*] Focus: Version Fingerprinting & Passive Exploit Mapping.{END}\n")

def run_step(step_num, title, command, wait_msg=None):
    print(f"{YELLOW}{BOLD}[Step {step_num}/3] {title}{END}")
    if wait_msg:
        print(f"{PINK}[i] {wait_msg}{END}")
    os.system(command)
    print(f"{GREEN}✔ Done.{END}\n")

def check_ping(target_host):
    cmd = f"ping -c 1 -W 2 {target_host} > /dev/null 2>&1" if os.name == 'posix' else f"ping -n 1 -w 2000 {target_host} > nul"
    return os.system(cmd) == 0

def analyze_results(folder):
    print(f"{PINK}{BOLD}" + "█"*20 + " PINK ANALYSIS SUMMARY " + "█"*20 + f"{END}")
    keywords = ["VULNERABLE", "CVE-", "Admin", "Config", "Backup", "Editable", "Password", "Exploit", "Apache", "Nginx", "PHP", ".env", "db_", "SQL", "allow_url_include"]
    found = False
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(folder, filename), 'r', errors='ignore') as f:
                    content = f.read()
                    for key in keywords:
                        if key.lower() in content.lower():
                            found = True
                            print(f"{PINK}{BOLD}[!] INTERESTING FINDING:{END} '{key}' in {filename}")
            except: continue
    if not found:
        print(f"{END}[*] No obvious critical keywords found.")
    print(f"{PINK}{BOLD}" + "█"*63 + f"{END}\n")

def main():
    show_banner()
    
    target = input(f"{TURQUOISE}{BOLD}» Enter Target URL or IP: {END}").strip()
    if not target: sys.exit()

    host_clean = target.replace("http://", "").replace("https://", "").split('/')[0]
    
    if not check_ping(host_clean):
        print(f"{RED}[!] Target unreachable or blocking ICMP. Proceeding with caution...{END}")

    default_wl = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.exists(default_wl):
        default_wl = "common.txt" if os.path.exists("common.txt") else ""

    wl_prompt = f"{TURQUOISE}{BOLD}» Wordlist Path (Enter for default: {default_wl}): {END}"
    wl_path = input(wl_prompt).strip() or default_wl
    
    if not wl_path or not os.path.exists(wl_path):
        print(f"{RED}[!] Wordlist error. File not found at: {wl_path}{END}")
        sys.exit()
    
    ext_choice = input(f"{TURQUOISE}{BOLD}» Deep Scan: Check file extensions? (y/n): {END}").lower().strip()
    ext_flag = "-e .php,.txt,.bak,.zip,.sql,.env" if ext_choice == 'y' else ""

    base_dir = f"recon_{host_clean.replace('.', '_')}"
    trash_dir = f"{base_dir}/debug_logs"
    for d in [base_dir, trash_dir]:
        if not os.path.exists(d): os.makedirs(d)

    print(f"\n{TURQUOISE}[*] Funnel initiated. Gathering data...{END}\n")

    run_step(1, "Web Tech Mapping", 
             f"whatweb --no-errors --open-timeout 10 -a 1 {target} > {base_dir}/1_fingerprint.txt 2> {trash_dir}/whatweb.err")

    run_step(2, "Service & Version Mapping", 
             f"nmap -F -sV -Pn --version-intensity 5 -T4 {host_clean} > {base_dir}/2_services.txt 2> {trash_dir}/nmap.err",
             "Identifying services and versions. Stay tuned...")

    ffuf_url = target if target.startswith("http") else f"http://{target}"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    
    run_step(3, "Directory & File Discovery", 
             f"ffuf -t 50 -u {ffuf_url}/FUZZ -w {wl_path} {ext_flag} -H 'User-Agent: {ua}' -mc 200,301,302 -o {base_dir}/3_fuzz_report.txt -s > {trash_dir}/ffuf_raw.log 2>&1",
             "Searching for hidden paths with Stealth UA. Finalizing report...")

    analyze_results(base_dir)
    
    print(f"{GREEN}{BOLD}✔ MISSION COMPLETE.{END}")
    print(f"{TURQUOISE}Main Reports: {base_dir}{END}")
    print(f"{TURQUOISE}Technical Logs: {trash_dir}{END}\n")

if __name__ == "__main__":
    main()
