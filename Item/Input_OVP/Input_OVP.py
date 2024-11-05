from ...Library.importer import *


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
        self.Load: List[float] = [0.0, 0.0]
        self.Transent_Volt = 0.0
        self.Input = Voltage_Data()
        self.TurnOnDelayTime: float = 0.0
        self.Check_After_Test = PowerOnCheckUnit()
        self.Check_Before_test = PowerOnCheckUnit()


class TestItem(ItemCore.TestItem):
    def __init__(self, Name: str = "", logUnit: LogUnit = LogUnit()) -> None:
        super().__init__(Name, logUnit)

    def PSU_Power_ON_and_Load_ON(self, caseB: LogUnit):
        for i in range(self.Test_Plan_Data.Sample_Size):
            PSUx[i].PSON.Set_Value(True)

        # Load & input setting & turn on (使用sag volt去判斷要吃的Load Cond., 避免觸動OCP)
        for i in range(len(caseB.Load)):
            Load[i].Load_CC_ON_Amp(caseB.Load[i] * PSU.get_LoadMax(i, caseB.Transent_Volt, caseB.Input.Frequency) / 100)

        Source[0].Sequence_ON_(caseB.Input)
        Delay(caseB.TurnOnDelayTime)

    def Power_ON_Check(self, case_C: PowerOnCheckUnit) -> bool:
        pf = True
        # Read FW status
        # PSU1
        for i in range(self.Test_Plan_Data.Sample_Size):
            pf &= case_C.Status79h[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Word().Value)
            pf &= case_C.Status7Ah[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Vout().Value)
            pf &= case_C.Status7Bh[i].SetMeasure_AutoJudge(PSUx[i].Read_Status_Iout().Value)
            pf &= case_C.Status7Ch[i].SetMeasure_AutoJudge(PSUx[i].Read_Input_Status().Value)

        while len(case_C.Vout) < len(Load):
            case_C.Vout.append(JudgementData_Float())

        # Read Vout/Vsb
        for i in range(len(Load)):
            pf &= case_C.Vout[i].SetMeasure_AutoJudge(Load[i].read_voltage())
        return pf

    def Run_Single_Condition(self, caseA: LogUnit):
        super().Run_Single_Condition(caseA)

        self.PSU_Power_ON_and_Load_ON(caseA)

        self.Power_ON_Check(caseA.Check_After_Test)
        self.Power_ON_Check(caseA.Check_Before_test)
        caseA.Scope_Setting
