# 🐍 python-humors

**Automation Scripts for Network CI/CD**

`python-humors` is a collection of Python utilities that assist with configuration validation, compliance checking, connectivity testing, and more—all tailored for **CI/CD pipelines in network engineering** environments. These scripts are designed to integrate into tools like GitHub Actions, GitLab CI, Jenkins, and Ansible.


## 📌 Purpose

This repository provides Python scripts to:
- Validate device configurations against golden baselines
- Render network configurations from templates (e.g., Jinja2)
- Test connectivity and neighbor relationships (e.g., BGP)
- Enforce compliance rules against configuration policy files
- Integrate into CI/CD workflows for automated testing and deployment


## 📁 Repository Structure

```
python-humors/
├── scripts/
│   ├── validate_configs.py         # Compare intended vs running configs
│   ├── check_compliance.py        # Audit config against policy rules
│   ├── render_templates.py        # Render configs from Jinja2 templates
│   ├── test_connectivity.py       # Ping or SSH reachability checks
│   ├── verify_bgp_neighbors.py    # Show and parse BGP summary output
│   └── README.md                  # Per-script usage instructions
├── tests/
│   ├── test_config_syntax.py      # Linting and syntax validation
│   └── test_compliance_rules.py   # Unit tests for compliance policies
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```


## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/python-humors.git
cd python-humors
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## 🛠 Script Overview

| Script                     | Description                                               |
|----------------------------|-----------------------------------------------------------|
| `validate_configs.py`      | Diffs golden config vs device config for mismatches       |
| `check_compliance.py`      | Compares device config to required rules in JSON/YAML     |
| `render_templates.py`      | Uses Jinja2 to generate configuration files dynamically    |
| `test_connectivity.py`     | Checks reachability between hosts via ping or Netmiko     |
| `verify_bgp_neighbors.py`  | Verifies BGP neighbor status via CLI command parsing      |


## ⚙️ GitHub Actions Integration

This repo includes a sample GitHub Actions pipeline under `.github/workflows/ci.yml`. It can be used to:

- Run unit tests on pull requests
- Lint and syntax-check scripts
- Simulate config rendering
- Alert on compliance violations

### Example `.github/workflows/ci.yml` (included)

```yaml
name: Python CI for Network Scripts

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests
      run: pytest tests/
```


## 🧪 Testing

Tests live in the `tests/` directory and are compatible with `pytest`.

```bash
pytest tests/
```


## 📦 Dependencies

Required packages are defined in `requirements.txt`. Includes:

- `netmiko`
- `jinja2`
- `pytest`
- `napalm` (optional)
- `pyyaml`
- `jsonschema`


## 🌐 Use Cases

- Pre-deployment validation for router/switch configs
- GitOps-style automation in enterprise networking
- Lab topology verification with GNS3, Mininet, or EVE-NG
- CI/CD integration in NetDevOps pipelines

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request


## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

## 📬 Contact

Created and maintained by Regis McCall — contributions welcome!
