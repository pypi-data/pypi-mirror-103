from typing import Type

from .baserule import BaseRule
from . import Rule


class SubDomainFields(BaseRule):
    min_qty: int


class SubdomainRule(Rule):
    fields: Type[BaseRule] = SubDomainFields

    @property
    def calc_weight(self):
        return self.bal if self.domain.name.count(".") > self.min_qty else 0
