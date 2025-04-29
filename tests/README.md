# ✅ Unit Tests for python-humors

This folder contains **automated unit and integration tests** for validating network automation scripts and configuration policies in the `python-humors` repository.

Tests are written in **Python using `pytest`**, and are intended to be run:
- **Locally** by developers and engineers
- **Automatically** via CI pipelines (GitHub Actions, GitLab CI, Jenkins, etc.)

---

## 🧪 Test Overview

| File                          | Purpose                                                |
|------------------------------|--------------------------------------------------------|
| `test_config_syntax.py`      | Basic validation of Cisco configuration files          |
| `test_compliance_rules.py`   | Verifies config contains all required compliance rules |

---

## 🔍 `test_config_syntax.py`

### ✅ What It Tests
- Whether the config file exists at the expected path (`scripts/examples/running.txt`)
- Whether the config contains illegal characters (e.g., null bytes)
- Whether any config lines are excessively long (line length > 500 chars)

### 📄 Sample Assertions

```python
assert os.path.exists(CONFIG_PATH)
assert '\x00' not in line
assert len(line) < 500
```

---

## 🔍 `test_compliance_rules.py`

### ✅ What It Tests
- Loads a device config (`running.txt`)
- Loads a YAML-based compliance policy (`policy.yaml`)
- Confirms that **every rule** in the policy exists in the config

### 📄 Compliance Format Example

**`policy.yaml`**

```yaml
- hostname R1
- ip ssh version 2
- service password-encryption
- login local
- transport input ssh
```

> These rules are checked for **exact string matches** inside the config.

---

## 📂 File Structure

```
tests/
├── test_config_syntax.py       # Config file exists, syntax/length check
├── test_compliance_rules.py    # Match policy rules to actual config
```

Dependencies and test targets:

```
scripts/
└── examples/
    ├── running.txt             # Actual device config to be validated
    └── policy.yaml             # Expected rules the config must include
```

---

## ▶️ Running Tests

From the root of the repo:

```bash
pytest tests/
```

Or run individual test files:

```bash
pytest tests/test_config_syntax.py
pytest tests/test_compliance_rules.py
```

Sample output:

```
=============================================================
tests/test_config_syntax.py::test_config_file_exists PASSED
tests/test_config_syntax.py::test_no_unexpected_characters PASSED
tests/test_config_syntax.py::test_lines_not_too_long PASSED
tests/test_compliance_rules.py::test_compliance_rules_present PASSED
=============================================================
```

---

## ⚙️ CI Integration

Add to `.github/workflows/ci.yml` or equivalent:

```yaml
- name: Run Python tests
  run: pytest tests/
```

---

## 📦 Dependencies

Make sure `requirements.txt` includes:

```txt
pytest>=7.4.0
pyyaml>=6.0
```

Install locally:

```bash
pip install -r requirements.txt
```

---

## 🔧 Optional Enhancements

Consider future improvements:
- Use **regex compliance rules** instead of exact strings
- Add **interface-specific policy checks**
- Validate **NTP, logging, and SNMP configs** per policy templates
- Add **pre/post diffs** for CI approval workflows

---

## 🙋 Support

If a test fails, double-check:
- That the config file is in the right place (`scripts/examples/running.txt`)
- That your policy rules in `policy.yaml` are formatted correctly
- That the line in your config is a literal match (unless regex is added)

---

## 📄 License

This test suite is part of the `python-humors` project and licensed under MIT.
