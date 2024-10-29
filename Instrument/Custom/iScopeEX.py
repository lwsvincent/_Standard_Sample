"""
此檔案定義示波器(ScopeEX)的Channel定義
"""

from typing import Any

# 專案繼承於CRPS
from Project._Standard_CRPS.Instrument.Custom import iScopeEX


from Core.Instrument_Driver.Extend_Instrument.ScopeEX.Utility.Utility_Setup import ProbeSetup


class DefaultChannelList(iScopeEX.DefaultChannelList):
    def __init__(self) -> None:
        super().__init__()
        self.PSON = ProbeSetup("PSON")
        self.Vout.Scope_Channel = iScopeEX.iScopeEX.Scope_Channel.CH1
        self.Vout.Scope_Channel = iScopeEX.iScopeEX.Scope_Channel.CH2


class ScopeEX_Data_Unit(iScopeEX.ScopeEX_Data_Unit):
    def __init__(self) -> None:
        super().__init__()
        self.Channels: DefaultChannelList = DefaultChannelList()


class ScopeEX(iScopeEX.ScopeEX):
    def __init__(self) -> None:
        super().__init__()
        self.ChannelList = DefaultChannelList()
