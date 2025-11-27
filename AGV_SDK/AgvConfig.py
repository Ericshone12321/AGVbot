# Rewriting the provided C# AGV classes into equivalent Python classes

class AgvAxis:
    def __init__(self):
        self.Enable = False
        self.Ready = False
        self.Moving = False
        self.Coupling = False
        self.Busy = False
        self.Error = False


class AgvAxisMain:
    def __init__(self):
        self.Enable = False
        self.Ready1 = False
        self.Ready2 = False
        self.Ready3 = False
        self.Coupling1 = False
        self.Coupling2 = False
        self.Moving = False
        self.Busy = False
        self.Error = False


class AgvRunConfig:
    def __init__(self, cfg=None):
        if cfg:
            self.Velo = cfg.Velo
            self.Acce = cfg.Acce
            self.Dece = cfg.Dece
            self.Jerk = cfg.Jerk
        else:
            self.Velo = 0
            self.Acce = 0
            self.Dece = 0
            self.Jerk = 0


class Agv2DCode:
    def __init__(self, code=999999999, angle=0):
        self.X = 0
        self.Y = 0
        self.A = angle
        self.Code = code


class AgvPosition:
    def __init__(self, x=0, y=0, a=0):
        self.X = x
        self.Y = y
        self.A = a


class AgvFlag:
    def __init__(self):
        self.IsReady = False
        self.IsServoON = False
        self.IsJogMode = False
        self.IsMoving = False
        self.IsLaserStop = False
        self.IsEmergencyStop = False
        self.IsRunPause = False
        self.IsScriptStart = False
        self.IsScriptFinish = False
        self.IsScriptStop = False
        self.IsScriptPause = False
        self.IsLaserEnable = False
        self.IsLaserWarnField2 = False
        self.IsLaserWarnField1 = False
        self.IsLaserProtField = False
        self.IsLaserCarStop = False
        self.IsChargeing = False
        self.IsLiftUp = False
        self.IsTurnMaxiPt = False
        self.IsTurnMiniPt = False


class AgvStatus:
    def __init__(self):
        self.State = "OFFLINE"
        self.Flag = AgvFlag()
        self.AxisM = AgvAxisMain()
        self.AxisB = AgvAxis()
        self.AxisR = AgvAxis()
        self.AxisL = AgvAxis()
        self.AxisUD = AgvAxis()
        self.AxisT = AgvAxis()


class AgvLogIndex:
    def __init__(self):
        self.IsRunning = False
        self.ScriptIndex = 0
        self.ScriptCode = 0
        self.RunIndex = 0
        self.ErrorRunIndex = 0
        self.ErrorCode = 0


class CommandItem:
    def __init__(self):
        # Placeholder for actual command structure
        pass


class AgvConfig:
    def __init__(self):
        self.Mileage = 0.0
        self.Battery = "OFFLINE"
        self.Location = AgvPosition()
        self.RunPara = AgvRunConfig()
        self.Attitude = Agv2DCode()
        self.Shelves = Agv2DCode()
        self.Status = AgvStatus()
        self.Log = AgvLogIndex()
        self.Script = []

# Example usage:
# agv = AgvConfig()
# print(agv.Status.Flag.IsReady)
