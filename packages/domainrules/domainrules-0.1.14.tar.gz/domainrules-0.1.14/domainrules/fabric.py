from domainrules import Domain, Rule
from domainrules.describe import AVAILABLE_RULES


class NewRule:
    @classmethod
    def build(cls, domain: Domain, data: dict) -> Rule:
        """Create rule from received dict
        {"type": "LevensteinRule", "bal": 100,
            "possible": 3, "base_name": "alphabank"}
        {"type": "RegexpRule", "bal": 5, "regexp": "al.*bank"}
        {"type": "SubstringRule", "bal": 25,
            "subwords": ["alpha", "abank", "alpha-support"]}
        """

        if data.get("type") in AVAILABLE_RULES:
            # Есть такой класс или переменная
            obj = AVAILABLE_RULES[data["type"]].cls
            data.pop("type")
            if obj.validate(**data):
                return obj(domain).set_rules(**data)

        return Rule(domain).set_rules(bal=0)
