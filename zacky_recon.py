import requests
import os
import subprocess
import concurrent.futures

# Function to check if a subdomain is active
def is_active(subdomain):
    response = os.system(f"ping -c 1 {subdomain} > /dev/null 2>&1")
    return response == 0

# Function to run feroxbuster
def run_feroxbuster(subdomain):
    feroxbuster_output_file = f"ferox-{subdomain}.csv"
    subprocess.run(["sudo", "feroxbuster", "-u", subdomain, "-w", "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", "-o", feroxbuster_output_file, "-t", "50"])

# Function to run OWASP ZAP passive scan
def run_zap_passive_scan(subdomain):
    output_file = f"zap-output-{subdomain}.txt"
    url_http = f"http://{subdomain}"
    url_https = f"https://{subdomain}"
    
    try:
        response_http = requests.get(url_http, timeout=5)
        response_https = requests.get(url_https, timeout=5)
    except requests.RequestException:
        # If an exception occurs, skip the scan
        return
    
    if response_http.status_code == 200:
        scan_url = url_http
        protocol = "HTTP"
    elif response_https.status_code == 200:
        scan_url = url_https
        protocol = "HTTPS"
    else:
        # If neither HTTP nor HTTPS works, skip the scan
        return
    
    print(f"Performing passive scan on {protocol}://{subdomain}")
    
    with open(output_file, "w") as output:
        subprocess.run(["/opt/zaproxy/zap.sh", "-cmd", "-quickurl", scan_url], stdout=output)

# Function to run the fast silent full port scan using nmap
def run_port_scan(target_domain):
    port_scan_output_file = f"port-{target_domain}.txt"
    subprocess.run(["sudo", "nmap", "-p-", "-T4", "-oG", port_scan_output_file, target_domain])

# Function to print the title
def print_title():
    title = r"""
   ______          _            _____                      
  |___  /         | |          |  __ \                     
     / / __ _  ___| | ___   _  | |__) |___  ___ ___  _ __  
    / / / _` |/ __| |/ / | | | |  _  // _ \/ __/ _ \| '_ \ 
   / /_| (_| | (__|   <| |_| | | | \ \  __/ (_| (_) | | | |
  /_____\__,_|\___|_|\_\\__, | |_|  \_\___|\___\___/|_| |_|
                         __/ |                             
                        |___/                              
                            

                                           
       __  _  _| _        o _|_|_     |  _     _ 
       |||(_|(_|(/_   \^/ |  |_| |    | (_)\_/(/_
                                       
                              
     """
    print(title)

# Main function
def main():
    print_title()

    choice = input("Choose scan type:\n1. Simple\n2. Specific\nEnter your choice (1/2): ")

    if choice == "1":
        scan_type = "simple"
    elif choice == "2":
        scan_type = "specific"
        template_path = input("Enter the template path: ")
    else:
        print("Invalid choice.")
        return

    target_domain = input("Enter the target domain: ")
    subdomains_file = f"{target_domain}_subdomains.txt"
    subprocess.run(["sudo", "subfinder", "-all", "-d", target_domain, "-o", subdomains_file])

    active_subdomains_file = f"{target_domain}_active_subdomains_1.txt"

    with open(subdomains_file, 'r') as subdomains, open(active_subdomains_file, 'w') as active_subdomains:
        subdomain_list = [line.strip() for line in subdomains]

        print("Checking active or not subdomains, be quiet brody...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            active_subdomain_list = list(filter(is_active, subdomain_list))
            active_subdomains.writelines([sub + '\n' for sub in active_subdomain_list])

    if scan_type == "simple":
        nuclei_output_file = f"nuclei-{target_domain}.txt"
        subprocess.run(["sudo", "nuclei", "-l", active_subdomains_file, "-o", nuclei_output_file])
    elif scan_type == "specific":
        nuclei_output_file = f"nuclei-{target_domain}.txt"
        subprocess.run(["sudo", "nuclei", "-l", active_subdomains_file, "-t", template_path, "-o", nuclei_output_file])

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
         executor.map(run_feroxbuster, active_subdomain_list)

    # Perform OWASP ZAP passive scan on each active subdomain
    for subdomain in active_subdomain_list:
        run_zap_passive_scan(subdomain)

    # Run the port scan
    run_port_scan(target_domain)

if __name__ == "__main__":
    main()
