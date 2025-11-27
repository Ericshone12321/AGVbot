import pyads
import logging
from .AgvEnum import *
from .AgvConfig import *
from .AgvCmdItem import *

class AgvAds():
    index_group = 0x4020
    index_offset = 7004
    
    def __init__(self, name, netID) -> None:
        self.name = name
        self.netID = netID
        self.AdsComm = pyads.Connection(self.netID, 801)
        self.IsConnect = False
        self.IsBusy = False
        self.IsCmdUsed = False
        self.CtrlQueue = []
        self.log = logging.getLogger("log")
    
    def Connect(self):
        
        try:
            self.AdsComm.open()
            if self.AdsComm.read_state() is not None:
                self.IsConnect = True
                self.log.info(f"Connect: Connect Car {self.name} Success")
                return AgvResult.OK
            else:
                self.IsConnect = False
                self.log.info(f"Connect: Connect Car {self.name} Failed")
                return AgvResult.NotConnected
            
        except:
            self.IsConnect = False
            self.log.info(f"Connect: Connect Car {self.name} Failed")
            self.DisConnect()
            return AgvResult.Error
        
    def DisConnect(self):
        self.AdsComm.close()
        self.IsConnect = False
        return AgvResult.OK
    
    def UpdateParam(self):
        cfg = AgvConfig()
        try:
            data = self.AdsComm.read(AgvAds.index_group, AgvAds.index_offset, pyads.PLCTYPE_ARR_DINT(300))

            self.IsCmdUsed = (data[21] != 0) or (data[22] != 0) or (data[23] != 0)
            
            cfg.Battery = data[11]
            cfg.Mileage = data[15]
            cfg.Location = self.UpdatePosition(data)
            cfg.RunPara = self.UpdateRunPara(data)
            cfg.Log = self.UpdateLogIndex(data)
            cfg.Attitude = self.UpdateCamera(data, CCDType.Down)
            cfg.Shelves = self.UpdateCamera(data, CCDType.Up)
            cfg.Status = self.UpdateStatus(data)
            cfg.Script = self.UpdateScript(data)

            return cfg
        except:
            pass
    
    def UpdatePosition(self, data:list) -> AgvPosition:
        p = AgvPosition()
        if not self.IsConnect: 
            return p
        try:
            p.X = data[12]
            p.Y = data[13]
            p.A = data[14]
        except:
            self.IsConnect = False
        return p
    
    def UpdateRunPara(self, data:list) -> AgvRunConfig:
        p = AgvRunConfig()
        if not self.IsConnect: 
            return p
        try:
            p.Velo = data[7]
            p.Acce = data[8]
            p.Dece = data[9]
            p.Jerk = data[10]
        except:
            self.IsConnect = False
        return p
    
    def UpdateLogIndex(self, data:list) -> AgvLogIndex:
        p = AgvLogIndex()
        if not self.IsConnect: 
            return p
        try:
            p.ScriptIndex = data[41]
            p.ScriptCode = data[42]
            p.RunIndex = data[43]
            p.ErrorRunIndex = data[44]
            p.ErrorCode = data[45]
        except:
            self.IsConnect = False
        return p
    
    def UpdateCamera(self, data:list, type:CCDType) -> Agv2DCode:
        p = Agv2DCode()
        if not self.IsConnect: 
            return p
        try:
            p.X = data[type.value]
            p.Y = data[type.value+1]
            p.A = data[type.value+2]/100
            p.Code = data[type.value+3]
        except:
            self.IsConnect = False
        return p
    
    def UpdateStatus(self, data:list) -> AgvStatus:
        p = AgvStatus()
        if not self.IsConnect: 
            return p
        try:
            p.Flag = self.UpdateFlag(data)
            p.AxisM = self.UpdateAxisM(data)
            p.AxisB = self.UpdateAxis(data, AxisType.AxisB)
            p.AxisR = self.UpdateAxis(data, AxisType.AxisR)
            p.AxisL = self.UpdateAxis(data, AxisType.AxisL)
            p.AxisUD = self.UpdateAxis(data, AxisType.AxisUD)
            p.AxisT = self.UpdateAxis(data, AxisType.AxisT)
            
            if p.Flag.IsReady:
                p.State = "STANDBY"
            elif p.Flag.IsMoving:
                p.State = "MOVING"
            elif p.Flag.IsJogMode:
                p.State = "MANUAL"
            elif p.Flag.IsServoON:
                p.State = "SERVO_OFF"
                
        except:
            self.IsConnect = False
        return p
    
    def UpdateFlag(self, data:list) -> AgvFlag:
        p = AgvFlag()
        if not self.IsConnect: 
            return p
        try:
            temp = self.DwordToBit(data[1])
            p.IsReady = temp[0]
            p.IsServoON = temp[1]
            p.IsMoving = temp[2]
            p.IsJogMode = temp[5]
            
            temp1 = self.DwordToBit(data[2])
            p.IsLaserStop = temp1[0]
            p.IsEmergencyStop = temp1[1]
            
            temp2 = self.DwordToBit(data[3])
            p.IsScriptStart = temp2[0]
            p.IsScriptFinish = temp2[1]
            p.IsScriptStop = temp2[2]
            p.IsScriptPause = temp2[5]
            p.IsRunPause = temp2[7]
            
            temp3 = self.DwordToBit(data[4])
            p.IsLaserEnable = temp3[0]
            p.IsLaserWarnField2 = temp3[1]
            p.IsLaserWarnField1 = temp3[2]
            p.IsLaserProtField = temp3[3]
            p.IsLaserCarStop = temp3[7]
            
            temp4 = self.DwordToBit(data[5])
            p.IsChargeing = temp4[0]
            p.IsLiftUp = temp4[1]
            p.IsTurnMaxiPt = temp4[2]
            p.IsTurnMiniPt = temp4[3]
            # print(temp4)
        except:
            self.IsConnect = False
        return p
    
    def UpdateAxisM(self, data:list) -> AgvAxisMain:
        p = AgvAxisMain()
        if not self.IsConnect: 
            return p
        try:
            temp = self.DwordToBit(data[6])
            p.Enable = temp[0]
            p.Ready1 = temp[1]
            p.Ready2 = temp[2]
            p.Ready3 = temp[3]
            p.Coupling1 = temp[11]
            p.Coupling2 = temp[12]
            p.Moving = temp[21]
            p.Busy = temp[22]
            p.Error = temp[23]
            
            
        except:
            self.IsConnect = False
        return p
    
    def UpdateAxis(self, data:list, type:AxisType) -> AgvAxis:
        p = AgvAxis()
        if not self.IsConnect: 
            return p
        try:
            temp = self.DwordToBit(data[type.value])
            p.Enable = temp[0] #0
            p.Ready = temp[1] #1
            p.Coupling = temp[11] #11
            p.Moving = temp[21]  #21
            p.Busy = temp[22]  #22
            p.Error = temp[23]  #23
        
        except:
            self.IsConnect = False
        return p
    
    def UpdateScript(self, data:list):
        script_list = []
        for i in range(200):
            temp = data[101+i]
            if temp == 0:
                break
            else:
                script_list.append(CommandItem(temp))
                temp = 0
    
    def DwordToBit(self, data:int) -> list:
        byte_data = data.to_bytes(4, byteorder='little', signed=True)
        bit_data = []
        _data = []
        
        for i, b in enumerate(byte_data):
            bits = format(b, '08b') 
            bits = bits[::-1]
            bit_data.append(bits)
        
        for i in range(len(bit_data)):
            for j in range(len(bit_data[i])):
                _data.append(bool(int(bit_data[i][j])))
        return _data


# if __name__ == "__main__":
#     agv = AgvAds("239", "192.168.100.239.1.1")
#     agv.Connect() 
#     time.sleep(1)
#     cfg = agv.UpdateParam()  
#     print(cfg) 
    