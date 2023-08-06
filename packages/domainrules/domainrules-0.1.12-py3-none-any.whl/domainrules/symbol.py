from typing import Type

from .baserule import BaseRule
from . import Rule


class SymbolFileds(BaseRule):
    symbol: str
    min_qty: int


class SymbolRule(Rule):
    fields: Type[BaseRule] = SymbolFileds

    @property
    def calc_weight(self):
        if self.domain.name.count(self.symbol) > self.min_qty:
            return self.bal
        return 0
