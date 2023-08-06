Describe rules for domain

Usage example:
```python
import json
from domainrules import Domain, Rule
from domainrules.fabric import NewRule

#1. Set rules decorators
domain = Domain("")
# default bal - 0
base_rule = Rule(domain).set_rules(bal=0)
system_domain_rules: list[dict]
for rule in system_domain_rules:
    rule_dict = json.loads(rule)
    base_rule = NewRule.build(base_rule, rule_dict)

#2. apply
system_domain_rules.name = "somedomain.com"
if system_domain_rules.weight > 50:
    print("Warning!")
```