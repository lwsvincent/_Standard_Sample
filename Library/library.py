from typing import overload, List
from Core.Instrument_Driver.Instrument_Interface import *
from Core.Tools.Tools import *
from Core.Instrument_Driver.Scope.iScope_Lib.Utility import *
from Core.Instrument_Driver.Extend_Instrument.ScopeEX.Utility import DefaultChannelList as DefltChanelList

# 專案繼承於CRPS
from Project._Standard_CRPS.Library.library import *


from ..Instrument.Sample import *

# 這裡定義了CRPS需要的內容

if "PSU1_PSON" in locals():
    PSU1.PSON = PSU1_PSON

    PSU.Output = [
        # Name   Volt    Current(Low/High)   Current數量需與Input數量相同
        PSU_Output("+12V", 12, [123, 90.16, 81.96, 123], 150, 1),
        PSU_Output("Vsb", 12, [3, 3, 3, 3], 5, 1),
        # PSU_Output("+12V", 12.2, [45.08, 45.08, 45.08], 50),
        # PSU_Output("Vsb", 3.3, [3, 3, 3], 5),
    ]

    PSU.Input = [
        # Name   Min     Normal  Max     Freq
        PSU_Intput("Vin", 180, 230, 264, 63),
        PSU_Intput("Vin", 110, 120, 140, 47),
        PSU_Intput("Vin", 80, 90, 109, 47),
        PSU_Intput("Vin", 150, 230, 310, 0),
    ]

    PSU1.I2C = I2C[0]
    PSU1.PSON = GPIO[0]
    PSU2.I2C = I2C[1]
    PSU2.PSON = GPIO[1]

PSUx = [PSU1, PSU2]


def sample_function():
    pass
