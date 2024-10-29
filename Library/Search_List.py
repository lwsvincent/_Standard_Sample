from Core.Main.Sub_Task import Main_Configuration_Unit
from Project._Standard_CRPS.Library.library import *

# Import Project：
# 如果Project有子資料夾，則用.來連接
Main_Configuration_Unit.main_Config.Import_Projects.insert(0, "_Standard_CRPS")
