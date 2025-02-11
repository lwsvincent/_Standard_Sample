from Core.Instrument_Driver.Instrument_Interface import *
from Core.Instrument_Driver.Instrument_InterfaceEX import *
from .Custom import iScopeEX

from Core.Instrument_Driver.Load.Chroma_632xx import Chroma_632xx
from Core.Instrument_Driver.Load.Chroma_636xx import Chroma_63600

from Core.Instrument_Driver.Chamber.GTC_800 import GTC_800
from Core.Instrument_Driver.Scope.Tektronix_MSO5X import Tektronix_MSO5X
from Core.Instrument_Driver.Source.Chroma_61509 import Chroma_61509
from Core.Instrument_Driver.Meter.Yokogawa_WT310 import Yokogawa_WT310

from Core.Instrument_Driver.Multi.Chroma_Multi import Chroma_A800043
from Core.Instrument_Driver.GPIO.Sub20_GPIO import Sub20_GPIO
from Core.Instrument_Driver.GPIO.Sub20_GPIO import SUB20_GPIO_PIN
from Core.Instrument_Driver.I2C.Sub20_I2C import Sub20_I2C

from Core.Instrument_Driver.Scope.iScope_Lib.iChannelCMD import Scope_Channel

# Chamber.append(GTC_800("ASRL8::INSTR"))

# Scope.append(Tektronix_MSO5X("TCPIP0::169.254.1.100::inst0::INSTR"))
# # Scope.append(Tektronix_MSO5X("TCPIP0::169.254.253.100::inst0::INSTR"))


# Source.append(Chroma_61509("GPIB0::30::INSTR"))

# Load.append(Chroma_632xx("GPIB0::3::INSTR"))
# Load.append(Chroma_63600("GPIB0::4::INSTR", 1))  # Load Index = 1

Meter.append(Yokogawa_WT310("GPIB0::1::INSTR"))

# Multi: List[Chroma_A800043] = []
# try:
#     Multi.append(Chroma_A800043("ASRL6::INSTR"))
# except:
#     Multi.append(Chroma_A800043("ASRL7::INSTR"))

# PSU1_PWOK = Sub20_GPIO("PSU1_PWOK", SUB20_GPIO_PIN.GPIO_23_PIN_25)
# PSU1_PSON = Sub20_GPIO("PSU1_PSON", SUB20_GPIO_PIN.GPIO_19_PIN_29)  # 隨便編的
# PSU2_PSON = Sub20_GPIO("PSU2_PSON", SUB20_GPIO_PIN.GPIO_18_PIN_30)  # 認真編的
# GPIO.append(PSU1_PSON)
# GPIO.append(PSU2_PSON)


# I2C.append(Sub20_I2C(0xB0))
# I2C.append(Sub20_I2C(0xB2))
# I2C.append(Sub20_I2C(0xB4))
# I2C.append(Sub20_I2C(0xB6))
# I2C.append(Sub20_I2C(0xB8))
# I2C.append(Sub20_I2C(0xBA))


# Scope_EX = iScopeEX.ScopeEX()
# Scope_EX.scopes.append(Scope[0])
# Scope_EX.multis.append(Multi[0])


# for mm in [Scope_Channel.CH3,Scope_Channel.CH4,Scope_Channel.CH5,Scope_Channel.CH6]:


#     r1= iScopeEX.iScopeEX.iScopeEX.Scope_Multi_Link()
#     r1.Scope = Scope[0]
#     r1.Multi = Multi[0]
#     r1.Scope_Channel = mm

#     Scope_EX.MultiLinks.append(r1)
