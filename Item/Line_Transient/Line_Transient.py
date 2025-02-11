from ...Library.importer import *


class Accuracy_Sampleunit(Serializable_Data):
    def __init__(self) -> None:
        super().__init__()
        self.Value = JudgementData_Float()
        self.Accuray = JudgementData_Float()


class PowerOnCheckUnit(Serializable_Data):
    def __init__(self) -> None:
        super().__init__()
        self.Vout = [JudgementData_Float()]
        self.Status79h = [JudgementData_Hex(Fill_Zero=4), JudgementData_Hex(Fill_Zero=4)]
        self.Status7Ah = [JudgementData_Hex(), JudgementData_Hex()]
        self.Status7Bh = [JudgementData_Hex(), JudgementData_Hex()]
        self.Status7Ch = [JudgementData_Hex(), JudgementData_Hex()]
        self.PassFail: bool = True


class LogUnit(ItemCore.LogUnit):
    def __init__(self) -> None:
        super().__init__()
        self.PSON = ["Low", "Low"]
        self.Load: List[float] = [0.0, 0.0]
        self.LoadA: List[float] = [0.0, 0.0]
        self.Input = Voltage_Data()
        self.Pin = Accuracy_Sampleunit()
        self.Vin = Accuracy_Sampleunit()
        self.Iin = Accuracy_Sampleunit()
        self.Pout: List[Accuracy_Sampleunit] = [Accuracy_Sampleunit(), Accuracy_Sampleunit()]
        self.Vout: List[Accuracy_Sampleunit] = [Accuracy_Sampleunit(), Accuracy_Sampleunit()]
        self.Iout: List[Accuracy_Sampleunit] = [Accuracy_Sampleunit(), Accuracy_Sampleunit()]
        self.Inst_Vin: float = 0.0
        self.Inst_Iin: float = 0.0
        self.Inst_Pin: float = 0.0
        self.I2C_Vin: float = 0.0
        self.I2C_Iin: float = 0.0
        self.I2C_Pin: float = 0.0
        self.TurnOnDelayTime: float = 0.0
        self.Transent_Volt = 0.0
        self.Check_After_Test = PowerOnCheckUnit()
        # FW Status
        self.FW_79h = JudgementData_Hex(Fill_Zero=4)
        self.FW_7Ah = JudgementData_Hex(Fill_Zero=2)
        self.FW_7Bh = JudgementData_Hex(Fill_Zero=2)
        self.FW_7Ch = JudgementData_Hex(Fill_Zero=2)


class TestItem(ItemCore.TestItem):
    def __init__(self, Name: str = "", logUnit: LogUnit = LogUnit()) -> None:
        super().__init__(Name, logUnit)

    def Parameter_Initial(self, case: LogUnit):
        for i in range(len(case.Load)):
            case.LoadA[i] = case.Load[i] * PSU.get_LoadMax(i, case.Input.Voltage, case.Input.Frequency) / 100

    def PSU_Power_ON_and_Load_ON(self, case: LogUnit):

        for i in range(self.Test_Plan_Data.Sample_Size):
            PSUx[i].PSON.Set_Value(True)

        # Load & input setting & turn on (使用sag volt去判斷要吃的Load Cond., 避免觸動OCP)
        for i in range(len(case.Load)):
            Load[i].Load_CC_ON_Amp(case.Load[i] * PSU.get_LoadMax(i, case.Transent_Volt, case.Input.Frequency) / 100)

        Source[0].Turn_ON(case.Input)
        Delay(case.TurnOnDelayTime)

    def Power_ON_Check(self, case: PowerOnCheckUnit) -> bool:
        pf = True
        # Read FW status
        # PSU1
        for i in range(self.Test_Plan_Data.Sample_Size):
            pf &= case.Status79h[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Word().Value)
            pf &= case.Status7Ah[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Vout().Value)
            pf &= case.Status7Bh[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Iout().Value)
            pf &= case.Status7Ch[i].SetMeasure_AutoJudge(PSUx[i].Read_Input_Status().Value)

        while len(case.Vout) < len(Load):
            case.Vout.append(JudgementData_Float())
        # Read Vout/Vsb
        for i in range(len(Load)):
            pf &= case.Vout[i].SetMeasure_AutoJudge(Load[i].read_voltage())
        return pf

        Vin_waveform = Scope[0].GetWaveformData(case.Scope_Setting.Channels.Vin.Scope_Channel)
        Alert_waveform = Scope[0].GetWaveformData(case.Scope_Setting.Channels.SMBAlert.Scope_Channel)
        timeunit = Scope[0].GetWaveformTimeUnit
        Channel_Y1 = case.Scope_Setting.Channels.Vin.Scope_Channel
        Channel_Y2 = case.Scope_Setting.Channels.SMBAlert.Scope_Channel

        x1_Vin = 0
        for vin in Vin_waveform:
            if vin > 300:
                break
            x1_Vin += 1
        Vin_X1_Position = x1_Vin * timeunit

        x2_SMBAlert = 0
        for SMBAlert in Alert_waveform:
            if SMBAlert > 1.7:
                break
            x2_SMBAlert += 1
        Alert_X2_Position = x2_SMBAlert * timeunit

        Timediff = Alert_X2_Position - Vin_X1_Position

        Scope[0].Cursor.set_Cursor_Sec_Volt(Vin_X1_Position, Alert_X2_Position, 300, 1.7, Channel_Y1, Channel_Y2)

        case.Measure_Time.SetMeasure_AutoJudge(Timediff)

        case.Picture = self.SavePicture(Scope[0], str(case.Index))
        case.Picture = Scope[0].SavePicture(self.GetImagePath(str(case.Index)))  # Save image

    def Read_Inst_I2C(self, case: LogUnit):
        case.Inst_Vin = Meter[0].Get_VoltageRMS()
        case.Inst_Iin = Meter[0].Get_CurrentRMS()
        case.Inst_Pin = Meter[0].Get_Power_Real()
        # case.I2C_Vin = PSU1.Read_Vin()
        # case.I2C_Iin = PSU1.Read_Iin()
        # case.I2C_Pin = PSU1.Read_Pout()
        case.I2C_Vin = 120
        case.I2C_Iin = 120
        case.I2C_Pin = 120

        Vout0_inst = Load[0].read_voltage()
        Vout0_I2C = PSU1.Read_Vout(0)

        Vout0_Accuracy = (Vout0_inst - Vout0_I2C) / Vout0_inst
        case.Vout[0].Accuray.SetMeasure_AutoJudge(Vout0_Accuracy)

        Vout1_inst = Load[1].read_voltage()
        Vout1_I2C = PSU1.Read_Vout(1)

        Vout1_Accuracy = (Vout1_inst - Vout1_I2C) / Vout1_inst
        case.Vout[1].Accuray.SetMeasure_AutoJudge(Vout1_Accuracy)

    def Calculation(self, case: LogUnit):
        Vin_Accuracy = (case.Inst_Vin - case.I2C_Vin) / case.Inst_Vin
        Iin_Accuracy = (case.Inst_Iin - case.I2C_Iin) / case.Inst_Iin
        Pin_Accuracy = (case.Inst_Pin - case.I2C_Pin) / case.Inst_Pin
        Vin_Value = abs(case.Inst_Vin - case.I2C_Vin)
        Iin_Value = abs(case.Inst_Iin - case.I2C_Iin)
        Pin_Value = abs(case.Inst_Pin - case.I2C_Pin)

        case.Vin.Accuray.SetMeasure_AutoJudge(Vin_Accuracy)
        case.Iin.Accuray.SetMeasure_AutoJudge(Iin_Accuracy)
        case.Pin.Accuray.SetMeasure_AutoJudge(Pin_Accuracy)
        case.Vin.Value.SetMeasure_AutoJudge(Vin_Value)
        case.Iin.Value.SetMeasure_AutoJudge(Iin_Value)
        case.Pin.Value.SetMeasure_AutoJudge(Pin_Value)

    def Run_Single_Condition(self, case: LogUnit):
        super().Run_Single_Condition(case)
        # self.Parameter_Initial(case)
        # PSU.PSU_OFF()
        # self.PSU_Power_ON_and_Load_ON(case)
        # self.Power_ON_Check(case.Check_After_Test)

        self.Read_Inst_I2C(case)
        self.Calculation(case)

        # case.PassFail = True
