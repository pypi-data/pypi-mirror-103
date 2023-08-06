from . import Rule
from .baserule import BaseRule
from .regexp import RegexpRule, RegexpFields
from .substring import SubstringRule, SubstringFields
from .symbol import SymbolRule, SymbolFileds
from .levenshtein import LevenshteinRule, LevenshteinFields
from .numbers import NumbersRule, NumbersFields
from .greendomain import GreenDomainRule, GreenDomainFields
from .reddomin import RedDomainRule, RedDomainFields
from .subdomain import SubdomainRule, SubDomainFields
from .domainemul import DomainEmulRule, DomainEmulFields


class RuleDescription:
    name: str
    cls: object
    validator: object

    def __init__(self, name: str = None, cls: Rule = None, validator: BaseRule = None):
        self.name = name
        self.cls = cls
        self.validator = validator


AVAILABLE_RULES = {
    'RegexpRule': RuleDescription("Detect by regexp", RegexpRule, RegexpFields),
    'SubstringRule': RuleDescription("Contain substring", SubstringRule, SubstringFields),
    'SymbolRule': RuleDescription("Substring count more than", SymbolRule, SymbolFileds),
    'LevenshteinRule': RuleDescription("Levenshtein distance to original", LevenshteinRule, LevenshteinFields),
    'NumbersRule': RuleDescription("Numbers in name", NumbersRule, NumbersFields),
    'GreenDomainRule': RuleDescription("Whitelist domain", GreenDomainRule, GreenDomainFields),
    'RedDomainRule': RuleDescription("Red domain", RedDomainRule, RedDomainFields),
    'SubdomainRule': RuleDescription("SubdomainRule rule", SubdomainRule, SubDomainFields),
    'DomainEmulRule': RuleDescription("Domain emulation", DomainEmulRule, DomainEmulFields),
}
