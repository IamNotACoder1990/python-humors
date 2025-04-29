import yaml
import threading
import logging
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime

# Setup logging
logfile = f"baseline_ssh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

print(f"[i] Logging to {logfile}")

# === 1. Load YAML Inventory ===
def load_inventory(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)["devices"]

# === 2. Build SSH Config Commands ===
def generate_baseline_commands(hostname, domain, ssh_user, ssh_pass):
    return [
        f"hostname {hostname}",
        f"ip domain-name {domain}",
        "crypto key generate rsa modulus 2048",
        "ip ssh version 2",
        "ip ssh logging events",
        f"username {ssh_user} privilege 15 secret {ssh_pass}",
        "line vty 0 4",
        " login local",
        " transport input ssh",
        "exit",
        "line vty 5 15",
        " exec-timeout 0 0",
        " transport input none",
        " transport output none"
    ]

# === 3. Worker Function for Each Device ===
def baseline_device(device, ssh_user, ssh_pass, domain):
    try:
        print(f"[+] Connecting to {device['name']} ({device['host']})...")
        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["host"],
            username=device["username"],
            password=device["password"],
        )
        conn.enable()

        # Device-specific hostname or fallback to name
        hostname = device.get("hostname", device["name"])
        cmds = generate_baseline_commands(hostname, domain, ssh_user, ssh_pass)
        output = conn.send_config_set(cmds)

        # Log success
        logging.info(f"[✔] Baseline successful on {device['name']} ({device['host']})")
        logging.info(output)
        print(f"[✔] Done: {device['name']}")

        conn.disconnect()

    except Exception as e:
        msg = f"[!] FAILED on {device['name']} ({device['host']}): {str(e)}"
        logging.error(msg)
        print(msg)

# === 4. Main Runner ===
def main():
    print("\n--- 🧩 BULK SSH BASELINE SCRIPT ---\n")

    inventory_path = "scripts/inventory.yaml"
    devices = load_inventory(inventory_path)

    ssh_user = input("New SSH Username: ")
    ssh_pass = getpass("New SSH Password: ")
    domain = input("Default Domain Name: ")

    threads = []
    for device in devices:
        t = threading.Thread(target=baseline_device, args=(device, ssh_user, ssh_pass, domain))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[✓] All threads complete.")
    print(f"[📄] Log saved to: {logfile}")

if __name__ == "__main__":
    main()
