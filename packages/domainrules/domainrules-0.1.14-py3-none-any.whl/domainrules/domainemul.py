"""
6.GreenDomain  удаляет все записи с субдоменами от указаного в парметрах
домена второго уровня. тоесть Greendomain amazon.com удалит server2.amazon.com
 и любые другие субдомены из списка до начала проверки на синтаксис.
"""
from typing import Type

from pydantic import BaseModel

from .baserule import BaseRule
from . import Rule


class DomainEmulFields(BaseRule):
    domain_part: str  # "com"


class DomainEmulRule(Rule):
    fields: Type[BaseModel] = DomainEmulFields

    @property
    def calc_weight(self):
        variants = [
            f"-{self.domain_part}.",
            f".{self.domain_part}.",
            f"-{self.domain_part}-",
        ]

        if any([p in self.domain.name for p in variants]):
            return self.bal

        return 0
