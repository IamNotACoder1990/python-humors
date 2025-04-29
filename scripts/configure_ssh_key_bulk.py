import yaml
import threading
import logging
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
import os

# Setup log file
logfile = f"configure_ssh_key_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

print(f"[i] Logging to {logfile}")

# === Load Inventory ===
def load_inventory(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)["devices"]

# === Build Config Commands ===
def configure_ssh_key_user(conn, user, privilege, key_string):
    return conn.send_config_set([
        f"username {user} privilege {privilege}",
        "ip ssh pubkey-chain",
        f" username {user}",
        "  key-string",
        *[f"   {line}" for line in key_string.strip().splitlines()],
        "  exit",
        " exit",
        "line vty 0 4",
        " login local",
        " transport input ssh"
    ])

# === Worker Thread Function ===
def configure_device(device, ssh_user, ssh_key, privilege):
    try:
        logging.info(f"Connecting to {device['name']} ({device['host']})...")
        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["host"],
            username=device["username"],
            password=device["password"]
        )
        conn.enable()
        output = configure_ssh_key_user(conn, ssh_user, privilege, ssh_key)
        logging.info(f"[✔] SSH key user configured on {device['name']}")
        logging.info(output)
        print(f"[✔] {device['name']} complete")
        conn.disconnect()
    except Exception as e:
        msg = f"[!] Failed on {device['name']} ({device['host']}): {e}"
        logging.error(msg)
        print(msg)

# === Main Entry ===
def main():
    print("\n--- 🔐 BULK SSH KEY USER CONFIG ---\n")

    inventory_path = "scripts/inventory.yaml"
    devices = load_inventory(inventory_path)

    ssh_user = input("SSH Username to create: ")
    privilege = input("Privilege (default 15): ") or "15"

    pubkey_path = input("Path to public key file (e.g., ~/.ssh/id_rsa.pub): ").strip()
    if not os.path.isfile(pubkey_path):
        print(f"[!] File not found: {pubkey_path}")
        return

    with open(pubkey_path, "r") as f:
        ssh_key = f.read()

    threads = []
    for device in devices:
        t = threading.Thread(target=configure_device, args=(device, ssh_user, ssh_key, privilege))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[✓] All devices processed.")
    print(f"[📄] Log saved to {logfile}")

if __name__ == "__main__":
    main()
