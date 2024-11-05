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
        self.PSON = ["Low", "Low"]

        self.Input = Voltage_Data()
        self.TurnOnDelayTime: float = 0.0

        self.Load: List[float] = [0.0, 0.0]
        self.LoadA: List[float] = [0.0, 0.0]

        self.Seq_Volt_List: List[float] = [0.0, 0.0]
        self.Seq_Duration_List: List[float] = [1.0, 1.0]
        self.Seq_StartDeg_List: List[float] = [0.0, 0.0]
        self.Seq_Cycle = 1
        self.Transent_Volt = 0.0
        self.Transent_Duration = 0.0
        self.Transent_StartDeg = 0.0

        self.Spec1: JudgementData_Float = JudgementData_Float()
        self.Spec2: JudgementData_Float = JudgementData_Float()
        self.Spec3: JudgementData_Float = JudgementData_Float()
        self.Spec4: JudgementData_Float = JudgementData_Float()
        self.Spec5: JudgementData_Float = JudgementData_Float()
        self.Spec6: JudgementData_Float = JudgementData_Float()
        self.Spec7: JudgementData_Float = JudgementData_Float()
        self.Spec8: JudgementData_Float = JudgementData_Float()

        # self.Check_Befroe_test = PowerOnCheckUnit()
        # self.Check_After_Turn_ON = PowerOnCheckUnit()
        self.Check_After_Test = PowerOnCheckUnit()

        self.Picture = ""
        self.Remark = ""


class TestItem(ItemCore.TestItem):
    def __init__(self, Name: str = "", logUnit: LogUnit = LogUnit()) -> None:
        super().__init__(Name, logUnit)

    def PLD_VinScale_Adjust(self, case: LogUnit):
        """
        此功能可以協助設定PLD下的Vin_Vertical scale,
        這樣User就不用在excel parameter裡面一直改Vin scale囉.
        """

        # 先找到實際上Vin所設定的channel.

        VIN_CH = case.Scope_Setting.Channels.Vin
        # 根據輸入電壓設置 Vin_Scale
        if case.Input.Frequency > 0:
            if case.Input.Voltage <= 120:
                Vin_Scale = 100
            elif case.Input.Voltage <= 240:
                Vin_Scale = 200
            else:
                Vin_Scale = 500
        else:
            if case.Input.Voltage <= 200:
                Vin_Scale = 100
            elif case.Input.Voltage <= 350:
                Vin_Scale = 200
            else:
                Vin_Scale = 200
        # 設置 Channel 的垂直範圍
        Scope[0].Set_ChannelVerticalRange(VIN_CH.Scope_Channel, Vin_Scale)

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

    def First_Run(self):
        super().First_Run()
        Scope[0].measurement_delete_all()
        Scope[0].Disable_All_Channels()

    def Parameter_Initial(self, case: LogUnit):
        case.Transent_Volt = case.Seq_Volt_List[0]
        case.Transent_Duration = case.Seq_Duration_List[0] * 1000
        case.Transent_StartDeg = case.Seq_StartDeg_List[0]
        # 使用sag volt去判斷要吃的Load Cond., 避免觸動OCP
        for i in range(len(case.Load)):
            case.LoadA[i] = case.Load[i] * PSU.get_LoadMax(i, case.Transent_Volt, case.Input.Frequency) / 100

    def Setup_Scope(self, case: LogUnit) -> bool:
        # Scope Setting
        Scope_EX.Set_Channel(case.Scope_Setting)
        Scope_EX.Set_Measure(case.Scope_Setting)
        Scope_EX.Set_Timebase(case.Scope_Setting)
        Scope_EX.Set_Trigger(case.Scope_Setting)
        # Scope[0].Cursor.Off()
        self.PLD_VinScale_Adjust(case)
        Scope[0].Trigger.Action(Trigger_Action.Auto)

        # 判斷Scope timebase, 如果>10S/Div就用滾動模式抓圖, 反之用single模式
        """
        #長時間的timebase會造成S/R下降, InputSource的Ext pulse width 太短會無法正常trigger. 
        #(5V的ext signal可能只會show 0.2V base on 12.5KS/s SR.威仁實測結果)
        """
        if Scope[0].Timebase.Scale <= 4:
            Scope[0].Trigger.Action(Trigger_Action.Single)
            if not Scope[0].WatiForTrigger_Ready(100):
                print("Scope is not ready")
                case.Fail_Description.append("Scope is not ready")
                return False

        else:
            Scope[0].Trigger.Action(Trigger_Action.Auto)
            Delay(Scope[0].Timebase.Scale * 2)  # pre-run timebase兩格
        return True

    def PSU_Power_ON_and_Load_ON(self, case: LogUnit):
        for i in range(self.Test_Plan_Data.Sample_Size):
            if case.PSON[i] == "Low":
                PSUx[i].PSON.Set_Value(True)
            else:
                PSUx[i].PSON.Set_Value(False)

        # Load & input setting & turn on (使用sag volt去判斷要吃的Load Cond., 避免觸動OCP)
        for i in range(len(case.Load)):
            Load[i].Load_CC_ON_Amp(case.Load[i] * PSU.get_LoadMax(i, case.Transent_Volt, case.Input.Frequency) / 100)

        Source[0].Sequence_ON_(case.Input)
        Delay(case.TurnOnDelayTime)

    def DO_PLD(self, case: LogUnit):

        # PLD執行
        All_Step = []
        for x in range(len(case.Seq_Volt_List)):
            PLD_Step: Source_Sequence_Step
            if case.Input.Frequency != 0:
                # AC_PLD
                PLD_Step = Source_Sequence_Step(case.Seq_Duration_List[x], case.Seq_Volt_List[x], case.Input.Frequency, 0, case.Seq_StartDeg_List[x])
            else:
                # DC_PLD
                PLD_Step = Source_Sequence_Step(case.Seq_Duration_List[x], 0, 0, case.Seq_Volt_List[x])
            All_Step.append(PLD_Step)

        Source[0].Sequence_Run(case.Seq_Cycle, 1, All_Step)

    def Wait_Scope_finished(self, case: LogUnit) -> bool:

        if Scope[0].Timebase.Scale <= 4:
            if not Scope[0].WatiForTrigger_Save(100):
                print("Scope is not save sucessful.")
                case.Fail_Description.append("Scope is not save sucessful.")
                return False

        else:
            TotalWaveformTime = Scope[0].Timebase.Scale * 10
            RemainingTime = TotalWaveformTime - Scope[0].Timebase.Scale * 2 + Scope[0].Timebase.Scale * 0.25  # 加上0.25格timebase buffer.
            print("等待" + str(RemainingTime) + "秒, 示波器滾動一張圖的時間.")
            Delay(RemainingTime)

        Scope[0].Trigger.Action(Trigger_Action.Stop)
        return True

    def Scope_Set_Cursor_and_Save_Picture(self, case: LogUnit):

        if case.Seq_Cycle == 1:
            Scope[0].Cursor.set_Cursor_Sec_Volt(0, case.Transent_Duration / 1000, Channel_Y=case.Scope_Setting.Channels.Vin.Scope_Channel, Channel_Y2=case.Scope_Setting.Channels.Vin.Scope_Channel)

        if case.Scope_Setting.Channels.External.Enable:
            Scope[0].Set_ChannelEnable(case.Scope_Setting.Channels.External.Scope_Channel, False)
        case.Picture = Scope[0].SavePicture(self.GetImagePath(str(case.Index)))  # Save image

    def Run_Single_Condition(self, case: LogUnit):
        super().Run_Single_Condition(case)

        self.Parameter_Initial(case)

        PSU.PSU_OFF()

        self.PSU_Power_ON_and_Load_ON(case)
        if not self.Setup_Scope(case):
            return
        self.DO_PLD(case)

        if self.Wait_Scope_finished(case) == False:
            return

        self.Power_ON_Check(case.Check_After_Test)
        self.Scope_Set_Cursor_and_Save_Picture(case)
        case.PassFail = True
        case.PassFail &= self.Judge_Scope_Measures(case)
        case.PassFail &= case.Check_After_Test.PassFail
