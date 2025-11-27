from enum import IntEnum


class CommandType(IntEnum):
    TurnRight90 = 50
    TurnRight180 = 60
    TurnLeft180 = 80
    TurnLeft90 = 70
    TrayLiftUp = 130
    TrayPutDown = 140
    TurnRight90ByTrayStop = 150
    TurnRight180ByTrayStop = 160
    TurnLeft90ByTrayStop = 170
    TurnLeft180ByTrayStop = 180
    OpenLaserEnable = 310
    CloseLaserEnable = 320
    AutoTrayLiftUp = 330
    AutoTrayPutDown = 340
    TrayRight90 = 350
    TrayRight180 = 360
    TrayLeft90 = 370
    TrayLeft180 = 380
    TrayLine = 280
    ScriptPause = 300
    WaitInSec = 500
    GoToChargStn = 6000
    GoAwayChargStn = 7000
    GoForwardInMeter = 10000
    ErrorCode = 60000  # 或用其他適當的錯誤碼


class CommandItem:
    def __init__(self, data):
        self.Type = None
        self.Parameter = 0
        self.data = data
        
        if self.data is None:
            return

        if self.data == CommandType.TurnRight90:
            self.Type = CommandType.TurnRight90
        elif self.data == CommandType.TurnRight180:
            self.Type = CommandType.TurnRight180
        elif self.data == CommandType.TurnLeft180:
            self.Type = CommandType.TurnLeft180
        elif self.data == CommandType.TurnLeft90:
            self.Type = CommandType.TurnLeft90
        elif self.data == CommandType.TrayLiftUp:
            self.Type = CommandType.TrayLiftUp
        elif self.data == CommandType.TrayPutDown:
            self.Type = CommandType.TrayPutDown
        elif self.data == CommandType.TurnRight90ByTrayStop:
            self.Type = CommandType.TurnRight90ByTrayStop
        elif self.data == CommandType.TurnRight180ByTrayStop:
            self.Type = CommandType.TurnRight180ByTrayStop
        elif self.data == CommandType.TurnLeft90ByTrayStop:
            self.Type = CommandType.TurnLeft90ByTrayStop
        elif self.data == CommandType.TurnLeft180ByTrayStop:
            self.Type = CommandType.TurnLeft180ByTrayStop
        elif self.data == CommandType.OpenLaserEnable:
            self.Type = CommandType.OpenLaserEnable
        elif self.data == CommandType.CloseLaserEnable:
            self.Type = CommandType.CloseLaserEnable
        elif self.data == CommandType.AutoTrayLiftUp:
            self.Type = CommandType.AutoTrayLiftUp
        elif self.data == CommandType.AutoTrayPutDown:
            self.Type = CommandType.AutoTrayPutDown
        elif self.data == CommandType.TrayRight90:
            self.Type = CommandType.TrayRight90
        elif self.data == CommandType.TrayRight180:
            self.Type = CommandType.TrayRight180
        elif self.data == CommandType.TrayLeft90:
            self.Type = CommandType.TrayLeft90
        elif self.data == CommandType.TrayLeft180:
            self.Type = CommandType.TrayLeft180
        elif self.data == CommandType.ScriptPause:
            self.Type = CommandType.ScriptPause
        elif 500 < self.data < 600:
            self.Type = CommandType.WaitInSec
            self.Parameter = self.data - 500
        elif 6100 <= self.data < 7000:
            self.Type = CommandType.GoToChargStn
            self.Parameter = self.data - 6000
        elif 7100 <= self.data < 8000:
            self.Type = CommandType.GoAwayChargStn
            self.Parameter = self.data - 7000
        elif self.data > 10000 : # and (self.data - 10000) % 100 == 0 and (self.data - 10000) // 100 <= 50:
            self.Type = CommandType.GoForwardInMeter
            self.Parameter = (data - 10000) #// 100
        else:
            self.Type = CommandType.ErrorCode
            self.Parameter = self.data

    @property
    def Code(self):
        if self.Type == CommandType.WaitInSec and 0 < self.Parameter < 100:
            return CommandType.WaitInSec + self.Parameter
        elif self.Type == CommandType.GoForwardInMeter and 0 < self.Parameter <= 50:
            return CommandType.GoForwardInMeter + self.Parameter * 100
        elif self.Type == CommandType.GoToChargStn and 100 <= self.Parameter < 1000:
            return CommandType.GoToChargStn + self.Parameter
        elif self.Type == CommandType.GoAwayChargStn and 100 <= self.Parameter < 1000:
            return CommandType.GoAwayChargStn + self.Parameter
        elif self.Type not in {
            CommandType.ErrorCode,
            CommandType.WaitInSec,
            CommandType.GoForwardInMeter,
            CommandType.GoToChargStn,
            CommandType.GoAwayChargStn
        }:
            return int(self.Type)
        else:
            return 0  # 錯誤碼
