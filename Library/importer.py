from Core.Tools.Tools import *
from Core.Instrument_Driver.Scope.iScope_Lib.Utility import *
from Core.Instrument_Driver.Instrument_Interface import *
from Core.Instrument_Driver.Instrument_InterfaceEX import *
from ..Instrument.Custom import iScopeEX
from .library import *
from ..Library import ItemCore
from Core.Main.Sub_Task.Test_Plan.Reader import LoadModuleFromFullPath,LoadModulePath
from Core.Main.Sub_Task import Main_Configuration_Unit
import enum
import os

PSU1 = PSUx_Unit()
PSU2 = PSUx_Unit()
PSUx = [PSU1,PSU2]

working_path = os.getcwd()
exec("from " + LoadModulePath("\\Project\\" + Main_Configuration_Unit.main_Config.ProjectName + "\\Library\\library.py" + " import *"))
LoadModuleFromFullPath("\\Project\\" + Main_Configuration_Unit.main_Config.ProjectName + "\\Instrument\\" + Main_Configuration_Unit.main_Config.Instrument_FileName)


class CursorSetting(Serializable_Data):
    def __init__(self, Channel: str, Level: float) -> None:
        super().__init__()
        self.ChannelSet = Channel
        self.Level = Level
        self.Slope = EdgeTriggerSlope.EITHER
