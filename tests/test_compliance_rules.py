import yaml
import pytest

CONFIG_PATH = "scripts/examples/running.txt"
POLICY_PATH = "scripts/examples/policy.yaml"

@pytest.fixture
def config_text():
    with open(CONFIG_PATH) as f:
        return f.read()

@pytest.fixture
def compliance_rules():
    with open(POLICY_PATH) as f:
        return yaml.safe_load(f)

def test_compliance_rules_present(config_text, compliance_rules):
    for rule in compliance_rules:
        assert rule in config_text, f"Missing compliance rule: '{rule}'"
