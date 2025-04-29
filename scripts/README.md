# 🧰 Python Scripts – Detailed Usage Guide

This folder contains standalone Python scripts designed for integration into network engineering CI/CD pipelines. Each script serves a unique function such as configuration validation, policy compliance, or protocol verification.

Here’s a complete breakdown of **external input files** each script relies on — along with those I haven’t yet provided — so you can generate or structure them for your `python-humors/scripts/` folder:

---

## 🧾 Required Files by Script

| Script                     | Required External Files                      | Status                  | Suggested Format                        |
|---------------------------|----------------------------------------------|--------------------------|-----------------------------------------|
| `validate_configs.py`     | ✅ `intended.txt`<br>✅ `running.txt`          | **Not yet provided**     | Plaintext Cisco config (`show run`)     |
| `check_compliance.py`     | ✅ `config.txt`<br>✅ `policy.json` or `.yaml` | **Policy file not provided** | JSON or YAML list of required strings |
| `render_templates.py`     | ✅ `template.j2`<br>✅ `vars.yaml`             | **Not yet provided**     | Jinja2 template + YAML variables        |
| `test_connectivity.py`    | (Optional) device IP list or inventory       | **Not yet provided**     | YAML or JSON (hostnames, IPs)           |
| `verify_bgp_neighbors.py` | ✅ Device credentials dictionary (inline or file) | **Inline only**     | Should allow external JSON/YAML creds   |


## 📂 Suggested Supporting Files You Should Add - Be a friend to yourself!

### 1. `intended.txt`  
Golden config (e.g., baseline Cisco config)

```text
hostname R1
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
```


### 2. `running.txt`  
Current device config (used for comparison)

```text
hostname R1
interface GigabitEthernet0/0
 ip address 192.168.1.10 255.255.255.0
 no shutdown
```


### 3. `policy.json`  
Compliance rules (must be present in config)

```json
[
  "service timestamps debug datetime msec",
  "service password-encryption",
  "banner login ^Authorized access only^",
  "snmp-server community public RO"
]
```

**Alternative (`policy.yaml`)**
```yaml
- service timestamps debug datetime msec
- service password-encryption
- banner login ^Authorized access only^
- snmp-server community public RO
```


### 4. `template.j2`  
Jinja2 template for a router config

```jinja2
hostname {{ hostname }}
interface {{ interface }}
 ip address {{ ip }} {{ mask }}
 no shutdown
```


### 5. `vars.yaml`  
Variables to render the above template

```yaml
hostname: R1
interface: GigabitEthernet0/0
ip: 192.168.10.1
mask: 255.255.255.0
```


### 6. `hosts.yaml` (Optional for `test_connectivity.py`)

```yaml
hosts:
  - name: R1
    ip: 192.168.10.1
  - name: R2
    ip: 192.168.10.2
```


### 7. `device_credentials.json` (Optional for `verify_bgp_neighbors.py`)

```json
{
  "device_type": "cisco_ios",
  "host": "10.1.1.1",
  "username": "admin",
  "password": "admin123"
}
```


## ✅ Summary

To fully run and test all current scripts, you still need to create:

- `intended.txt`
- `running.txt`
- `policy.json` or `.yaml`
- `template.j2`
- `vars.yaml`
- *(optional)* `hosts.yaml` and `device_credentials.json`


## 📄 `validate_configs.py`

### 🔍 Purpose
Compare an **intended (golden)** configuration file with an **actual (running)** configuration to identify mismatches line-by-line.

### 📌 Use Case
- Ensure deployed router/switch configs match golden templates
- Prevent unauthorized changes before deployment

### 📥 Inputs
- `intended.txt`: Golden config
- `running.txt`: Actual config (e.g., pulled via Netmiko)

### 📤 Output
- Prints unified diff to console (or can be logged/exported)

### ▶️ Example Usage

```bash
python3 validate_configs.py
```

_(Edit the script to load `intended.txt` and `running.txt` paths or refactor to use argparse for dynamic input)_


## 📄 `check_compliance.py`

### 🔍 Purpose
Check a device config against required policy rules (ACLs, banners, SNMP, etc.) defined in a structured JSON or YAML file.

### 📌 Use Case
- Enforce security or compliance policies (e.g., required SNMP settings, mandatory NTP servers)

### 📥 Inputs
- `config.txt`: Device config file
- `policy.json` or `policy.yaml`: Rule file (list of required strings)

### 📤 Output
- Prints list of **missing/violated** rules

### ▶️ Example Usage

```bash
python3 check_compliance.py
```

_(Script loads `config.txt` and `policy.json` by default, modify as needed or add CLI support)_


## 📄 `render_templates.py`

### 🔍 Purpose
Render configuration files dynamically using **Jinja2 templates** and variable files.

### 📌 Use Case
- Auto-generate device configs (router/switch) from central templates
- Enable GitOps-style deployment using versioned input vars

### 📥 Inputs
- `template.j2`: Jinja2 config template
- `vars.yaml`: YAML file with substitution variables

### 📤 Output
- Rendered configuration (printed or saved to file)

### ▶️ Example Usage

```bash
python3 render_templates.py
```

_(Modify template and variable paths as needed or enhance the script with CLI support)_


## 📄 `test_connectivity.py`

### 🔍 Purpose
Perform basic reachability testing between network devices (ping or SSH).

### 📌 Use Case
- Validate host-to-host connectivity pre/post change
- Ensure SSH access for automation tooling (Netmiko)

### 📥 Inputs
- Host IP addresses or device dictionary (in-code or JSON/YAML)

### 📤 Output
- Ping or SSH result per host

### ▶️ Example Usage

```bash
python3 test_connectivity.py
```

_(Can be extended to load IPs from a file or inventory)_


## 📄 `verify_bgp_neighbors.py`

### 🔍 Purpose
Connect to a Cisco router (via SSH) and run `show ip bgp summary`, parsing neighbor status and session states.

### 📌 Use Case
- CI check for BGP neighbor health post-change
- Validate all neighbors are **Established**

### 📥 Inputs
- Device credentials (inline or from inventory JSON/YAML)

```python
router = {
    "device_type": "cisco_ios",
    "host": "10.0.0.1",
    "username": "admin",
    "password": "yourpass"
}
```

### 📤 Output
- CLI output showing BGP summary table

### ▶️ Example Usage

```bash
python3 verify_bgp_neighbors.py
```


## ✅ Tips for Integration

All scripts can be:
- Wrapped in shell or Ansible tasks
- Scheduled in Jenkins/GitHub Actions
- Enhanced with `argparse` for CLI flags
- Unit-tested via the `tests/` directory


## 📦 Required Python Packages

Install dependencies before running scripts:

```bash
pip install -r ../requirements.txt
```


## 📬 Need Help?

Open an issue or request enhancements via pull request. These scripts are designed to be modular and extensible.
