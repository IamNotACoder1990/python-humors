import json

def check_acl_compliance(config, policy_rules):
    violations = []
    for rule in policy_rules:
        if rule not in config:
            violations.append(rule)
    return violations

# Load from files and run
# violations = check_acl_compliance(open("config.txt").read(), json.load(open("policy.json")))
