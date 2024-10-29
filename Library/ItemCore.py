from Core import ItemCore
from ..Instrument.Custom import iScopeEX
from . import library
from typing import List


class LogUnit(ItemCore.LogUnit):
    def __init__(self) -> None:
        super().__init__()
        self.Scope_Setting = iScopeEX.ScopeEX_Data_Unit()
        self.VoutName: List[str] = []
        for vout in library.PSU.Output:
            self.VoutName.append(vout.Name)


class TestItem(ItemCore.TestItem):

    def First_Run(self):
        super().First_Run()

    pass
