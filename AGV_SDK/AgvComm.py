import pyads
import time
import logging
from .AgvAds import *
from .AgvEnum import *
from threading import Thread

class AgvComm:
    __ads_list: list = [] #模擬private static
    __config_list: list = []
    thread_list = []
    isCmdHandleTerminated = False
    
    @staticmethod
    def AddAgv(name: str, netID: str):
        log = logging.getLogger("log")
        log.info(f"AddAgv: Start connect Car {name}")
        
        try: 
            AgvComm.__ads_list.append(AgvAds(name, netID))
            AgvComm.__config_list.append(AgvConfig())
            
            index = len(AgvComm.__ads_list) - 1
            thread = Thread(target=AgvComm.AgvCmdHandle, args=(index,), daemon=True)
            thread.start()
            AgvComm.thread_list.append(thread)
            
            log.info(f"AddAgv: Add Car {name} success")
        except Exception as e:
            log.info(f"AddAgv: Connect Car {name} failed: {e}")
        
    @staticmethod
    def DisConnect():
        AgvComm.isCmdHandleTerminated = True
        if len(AgvComm.thread_list) != 0:
            try:
                for t in AgvComm.thread_list:
                    t.join()
            except:
                pass
    
    @staticmethod
    def GetAgvCfg(carID:str):
        index = next((i for i, x in enumerate(AgvComm.__ads_list) if x.name == carID), -1)
        
        if index == -1:
            return None
        else: 
            return AgvComm.__config_list[index]
    
    #===============基本功能=====================
    @staticmethod
    def ReadyMode(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Ready)
    
    @staticmethod
    def SearchMode(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Search)
    
    @staticmethod
    def MoveMode(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Move)
    
    @staticmethod
    def AutoRun(carID:str, distance:int) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Run_Auto, data=distance)
    
    @staticmethod
    def MotorRun(carID:str, distance:int) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Run_Motor, data=distance)
    
    @staticmethod
    def MotorStop(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Reset_Motor_Stop)
    
    @staticmethod
    def TrayStopTurnLeft90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Stop_Turn_Left_90)
    
    @staticmethod
    def TrayStopTurnLeft180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Stop_Turn_Left_180)
    
    @staticmethod
    def TrayStopTurnRight90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Stop_Turn_Right_90)
    
    @staticmethod
    def TrayStopTurnRight180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Stop_Turn_Right_180)
    
    @staticmethod
    def TurnLeft90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Turn_Left_90)
    
    @staticmethod
    def TurnLeft180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Turn_Left_180)
    
    @staticmethod
    def TurnRight90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Turn_Right_90)
    
    @staticmethod
    def TurnRight180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Turn_Right_180)
    
    
    @staticmethod
    def TrayLiftUp(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Lift_Up)
    
    @staticmethod
    def TrayPutDown(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Put_Down)
    
    @staticmethod
    def AutoTrayLiftUp(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Auto_Tray_Lift_Up)
    
    @staticmethod
    def AutoTrayPutDown(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Auto_Tray_Put_Down)
    
    @staticmethod
    def TrayTurnLeft90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Turn_Left_90)
    
    @staticmethod
    def TrayTurnLeft180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Turn_Left_180)
    
    @staticmethod
    def TrayTurnRight90(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Turn_Right_90)
    
    @staticmethod
    def TrayTurnRight180(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Turn_Right_180)
    
    #====充電功能====
    @staticmethod
    def GoToChargStn(carID:str, dist:int) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Go_To_Charge_Station, data=dist)
    
    @staticmethod
    def GoAwayChargStn(carID:str, dist:int) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Go_Away_Charge_Station, data=dist)

    #====JOG功能====
    @staticmethod
    def OpenJSEnable(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Open_Jog_Search_Enable)
    
    @staticmethod
    def CloseJSEnable(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Close_Jog_Search_Enable)
    
    @staticmethod
    def JogStart(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Jog_Start)
    
    @staticmethod
    def JogEnd(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Jog_End)
    
    @staticmethod
    def JogForward(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Jog_Forward)
    
    @staticmethod
    def JogBackward(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Jog_Backward)
    
    @staticmethod
    def JogLeft(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Jog_Left)
    
    @staticmethod
    def JogRight(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Jog_Right)
    
    #====相機功能====
    @staticmethod
    def Capture(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Capture)
    
    @staticmethod
    def ShelvesCapture(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Shelves_Capture)
    
    
    
    #====交管控制====
    @staticmethod
    def CarPause(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.CarPause)
    
    @staticmethod
    def CaeContinue(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.CarContinue)
    
    #====校正功能====
    @staticmethod
    def DistanceCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Correction_Distance)
    
    @staticmethod
    def AttitudeCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Correction_Attitude)
    
    @staticmethod
    def ShelvesDisCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Shelves_Correction_Distance)
    
    @staticmethod
    def ShelvesAttCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Shelves_Correction_Attitude)
    
    @staticmethod
    def TrayPutDownCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Correction_Tray_Down)
    
    @staticmethod
    def TrayRotateCorr(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Correction_Tray_Rotate)
    
    @staticmethod
    def TrayLine(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Tray_Line)
    
    #====腳本功能====
    @staticmethod
    def Start(carID:str, cmdList:list) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Script_Start, cmdList=cmdList)
    
    @staticmethod
    def Loop(carID:str, cmdList:list) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Mode_Move, cmdList=cmdList)
    
    @staticmethod
    def Pause(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Reset_Pause)
    
    @staticmethod
    def Stop(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Reset_Stop)
    
    @staticmethod
    def Continue(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Reset_Cont)
    
    @staticmethod
    def Reset_Loop(carID:str) -> AgvResult:
        return AgvComm.CommandCenter(carID=carID, cmd=AgvCmd.Reset_Loop)
    
    #================指令通訊================================
    @staticmethod
    def GetAgvIndex(carID:str) -> int:
        index = next((i for i, x in enumerate(AgvComm.__ads_list) if x.name == carID), -1)
        return index
      
    @staticmethod
    def CommandCenter(carID:str, cmd:AgvCmd, data:int = 0, cmdList:list[CommandItem] = None) -> AgvResult:
        if cmdList is None:
            cmdList = []
            
        log = logging.getLogger("log")
        index = AgvComm.GetAgvIndex(carID)
        
        if index != -1:
            ads = AgvComm.__ads_list[index]
        else:
            log.info(f"Command Center: Index Error")
            return AgvResult.Error
        
        if not ads.IsConnect:
            log.info(f"Command Center: NotConnected")
            return AgvResult.NotConnected
        
        def handle_reset(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            try:
                ads.CtrlQueue.clear()
                ads.IsBusy = False
                ads.AdsComm.write(0x4020, 7004 + 303 * 4, AgvComm.BitToDword(cmd.value - 30300), pyads.PLCTYPE_DWORD)
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            except Exception as e:
                log.info(f"Command Center: Error: {e}")
                return AgvResult.Error

        def handle_jog(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            try:
                cfg = AgvComm.__config_list[index]
                if not cfg.Status.Flag.IsJogMode:
                    return AgvResult.InvalidMode
                
                ads.AdsComm.write(0x4020, 7004 + 303 * 4, AgvComm.BitToDword(cmd.value - 30300), pyads.PLCTYPE_DWORD)
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            except Exception as e:
                log.info(f"Command Center: Error: {e}")
                return AgvResult.Error
            

        def handle_turn(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                cfg = AgvComm.__config_list[index]
                if cfg.Status.Flag.IsEmergencyStop:
                    log.info(f"Command Center: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                if not cfg.Status.Flag.IsServoON:
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Mode_Ready))
                
                ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_laser(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            try:
                ads.AdsComm.write(0x4020, 7004 + 303 * 4, AgvComm.BitToDword(cmd.value - 30300), pyads.PLCTYPE_DWORD)
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            except Exception as e:
                log.info(f"Command Center: Error: {e}")
                return AgvResult.Error
        
        def handle_carpause(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            try:
                ads.AdsComm.write(0x4020, 7004 + 304 * 4, AgvComm.BitToDword(cmd.value - 30400), pyads.PLCTYPE_DWORD)
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            except Exception as e:
                log.info(f"Command Center: Error: {e}")
                return AgvResult.Error
        
        def handle_runreset(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            try:
                ads.AdsComm.write(0x4020, 7004 + 301 * 4, AgvComm.BitToDword(cmd.value - 30100), pyads.PLCTYPE_DWORD)
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            except Exception as e:
                log.info(f"Command Center: Error: {e}")
                return AgvResult.Error
        
        def handle_search(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                cfg = AgvComm.__config_list[index]
                if cfg.Status.Flag.IsEmergencyStop:
                    log.info(f"Command Center: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_capture(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                
                log.info(f"Command Center: {cmd.name}")
                return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_autorun(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                if data < 1000 or data > 100000:
                    return AgvResult.InvalidAgvParam
                else:
                    cfg = AgvComm.__config_list[index]
                    if cfg.Status.Flag.IsEmergencyStop:
                        log.info(f"Command Center: Car {carID} Emergency Stop")
                        return AgvResult.Error
                    
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Send_Dis_AutoRun, data=data))
                    if not cfg.Status.Flag.IsServoON:
                        ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Mode_Ready))
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                    log.info(f"Command Center: {cmd.name}, {data}")
                    return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_motorrun(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                if data < -50000 or data > 50000:
                    log.info(f"Command Center: Invalid Param")
                    return AgvResult.InvalidAgvParam
                else:
                    cfg = AgvComm.__config_list[index]
                    if cfg.Status.Flag.IsEmergencyStop:
                        return AgvResult.Error
                    
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Send_Dis_MotorRun, data=data))
                    if not cfg.Status.Flag.IsServoON:
                        ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Mode_Ready))
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                    log.info(f"Command Center: {cmd.name}, {data}")
                    return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_charge(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                if data < 0 or data > 1000:
                    log.info(f"Command Center: Invalid Param")
                    return AgvResult.InvalidAgvParam
                else:
                    cfg = AgvComm.__config_list[index]
                    if cfg.Status.Flag.IsEmergencyStop:
                        log.info(f"Command Center: Car {carID} Emergency Stop")
                        return AgvResult.Error
                    
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Send_Dis_Charge, data=data))
                    if not cfg.Status.Flag.IsServoON:
                        ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Mode_Ready))
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                    log.info(f"Command Center: {cmd.name}, {data}")
                    return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_script(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            if not AgvComm.CheckCmdValid(cmdList):
                return AgvResult.InvalidAgvParam
            
            if len(ads.CtrlQueue) == 0 and not ads.IsBusy and not ads.IsCmdUsed:
                cfg = AgvComm.__config_list[index]
                if cmdList is None or len(cmdList) > 200:
                    log.info(f"Command Center: Invalid Param")
                    return AgvResult.InvalidAgvParam
                else:
                    if cfg.Status.Flag.IsEmergencyStop:
                        log.info(f"Command Center: Car {carID} Emergency Stop")
                        return AgvResult.Error

                    try:
                        # 建立要寫入的暫存區
                        for i, cmd1 in enumerate(cmdList):
                            ads.AdsComm.write(0x4020, 7004+(401+i)*4, cmd1.Code, pyads.PLCTYPE_DINT)
                        ads.AdsComm.write(0x4020, 7004 + 330 * 4, 1, pyads.PLCTYPE_UDINT)
                    except Exception as e:
                        log.info(f"Command Center: Error: {e}")
                        return AgvResult.Error
                    
                    if not cfg.Status.Flag.IsServoON:
                        ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=AgvCmd.Mode_Ready))
                    ads.CtrlQueue.append(lambda: AgvComm.HandleCmd(carID=carID, cmd=cmd))
                    
                    log.info(f"Command Center: {cmd.name}")
                    return AgvResult.OK
            else:
                log.info("Command Center: ADS Busy")
                return AgvResult.Busy 
        
        def handle_unknown(cmd: AgvCmd, data: int, cmdList: list[CommandItem]):
            log.info("Command Center: Unknown Command")
            return AgvResult.Error

        # 建立 command handler 對應表
        command_handlers = {
            AgvCmd.Reset_Stop: handle_reset,
            AgvCmd.Reset_Motor_Stop: handle_reset,
            AgvCmd.Jog_Forward: handle_jog,
            AgvCmd.Jog_Backward: handle_jog,
            AgvCmd.Jog_Left: handle_jog,
            AgvCmd.Jog_Right: handle_jog,
            AgvCmd.Jog_Move_Stop:handle_jog,
            AgvCmd.Open_Jog_Search_Enable : handle_laser,
            AgvCmd.Close_Jog_Search_Enable : handle_laser,
            AgvCmd.Open_Laser_Enable : handle_laser,
            AgvCmd.Close_Laser_Enable : handle_laser,
            AgvCmd.Mode_Jog_Start : handle_laser,
            AgvCmd.Mode_Jog_End : handle_laser,
            AgvCmd.Reset_Loop : handle_laser,
            AgvCmd.Reset_Pause : handle_laser,
            AgvCmd.Reset_Cont : handle_laser,
            AgvCmd.Reset_Cancel : handle_laser,
            AgvCmd.Reset_Error_Flag : handle_laser,
            AgvCmd.CarPause : handle_carpause,
            AgvCmd.CarContinue : handle_carpause,
            AgvCmd.Run_Reset_To_Code : handle_runreset,
            AgvCmd.Mode_Search : handle_search,
            AgvCmd.Mode_Move : handle_search,
            AgvCmd.Mode_Ready : handle_capture,
            AgvCmd.Capture: handle_capture,
            AgvCmd.Shelves_Capture: handle_capture,
            AgvCmd.Turn_Right_180 : handle_turn,
            AgvCmd.Turn_Right_90 : handle_turn,
            AgvCmd.Turn_Left_180 : handle_turn,
            AgvCmd.Turn_Left_90 : handle_turn,
            AgvCmd.Tray_Stop_Turn_Left_180 : handle_turn,
            AgvCmd.Tray_Stop_Turn_Left_90 : handle_turn,
            AgvCmd.Tray_Stop_Turn_Right_180 : handle_turn,
            AgvCmd.Tray_Stop_Turn_Right_90 : handle_turn,
            AgvCmd.Correction_Distance : handle_turn,
            AgvCmd.Correction_Attitude : handle_turn,
            AgvCmd.Shelves_Correction_Distance : handle_turn,
            AgvCmd.Shelves_Correction_Attitude : handle_turn,
            AgvCmd.Correction_Tray_Down : handle_turn,
            AgvCmd.Correction_Tray_Rotate : handle_turn,
            AgvCmd.Tray_Turn_Right_90 : handle_turn,
            AgvCmd.Tray_Turn_Right_180 : handle_turn,
            AgvCmd.Tray_Turn_Left_90 : handle_turn,
            AgvCmd.Tray_Turn_Left_180 : handle_turn,
            AgvCmd.Tray_Line : handle_turn,
            AgvCmd.Auto_Tray_Lift_Up : handle_turn,
            AgvCmd.Auto_Tray_Put_Down : handle_turn,
            AgvCmd.Tray_Lift_Up : handle_turn,
            AgvCmd.Tray_Put_Down : handle_turn,
            AgvCmd.Run_Auto : handle_autorun,
            AgvCmd.Run_Motor : handle_motorrun,
            AgvCmd.Go_To_Charge_Station : handle_charge,
            AgvCmd.Go_Away_Charge_Station : handle_charge,
            AgvCmd.Script_Loop : handle_script,
            AgvCmd.Script_Start : handle_script
        }

        # 呼叫方式
        handler = command_handlers.get(cmd, handle_unknown)
        return handler(cmd, data, cmdList)
    
    
    @staticmethod
    def CheckCmdValid(cmds:list[CommandItem]) -> bool:
        for cmd in cmds:
            if cmd.Type == CommandType.WaitInSec or cmd.Type == CommandType.GoForwardInMeter:
                if cmd.Parameter == 0: return False
                elif cmd.Type == CommandType.WaitInSec and cmd.Parameter > 100: return False
                elif cmd.Type == CommandType.GoForwardInMeter and cmd.Parameter > 50: return False
                else: return True
            else: 
                return True
  
    @staticmethod
    def BitToDword(index:int) -> int:
        value = 1 << index 
        byte_data = value.to_bytes(4, byteorder='little', signed=False)
        restored_value = int.from_bytes(byte_data, byteorder='little', signed=True)
        return restored_value
    
    @staticmethod
    def HandleCmd(carID:str, cmd:AgvCmd, data:int = 0) -> AgvResult:
        log = logging.getLogger("log")
        
        index = AgvComm.GetAgvIndex(carID)
        if index == -1:
            log.info(f"Command Handle: Index Error")
            return AgvResult.Error
        
        ads = AgvComm.__ads_list[index]
        
        if ads is None:
            log.info(f"Command Handle: Not Connect")
            return AgvResult.Error
        if not ads.IsConnect:
            log.info(f"Command Handle: Not Connect")
            return AgvResult.NotConnected
        
        cfg = AgvComm.__config_list[index]
        
        def handle_mode(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.IsBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 301 * 4, AgvComm.BitToDword(cmd.value - 30100), pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e:
                ads.IsBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_script(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.IsBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 303 * 4, AgvComm.BitToDword(cmd.value - 30300), pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e:
                ads.IsBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_move(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.isBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 302 * 4, AgvComm.BitToDword(cmd.value - 30200), pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e:
                ads.isBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_sendautorun(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.IsBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 321 * 4, data, pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e: 
                ads.IsBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_sendmotorrun(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.IsBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 322 * 4, data, pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e:
                ads.IsBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_sendcharge(cmd: AgvCmd, data: int):
            try:
                if cfg.Status.Flag.IsEmergencyStop:
                    ads.IsBusy = False
                    log.info(f"Command Handle: Car {carID} Emergency Stop")
                    return AgvResult.Error
                
                ads.AdsComm.write(0x4020, 7004 + 323 * 4, data, pyads.PLCTYPE_DINT)
                ads.IsBusy = False
                
                log.info(f"Command Handle: {cmd}, Done")
                return AgvResult.OK
            except Exception as e:
                ads.IsBusy = False
                log.info(f"Command Handle: Error: {e}")
                return AgvResult.Error
        
        def handle_unknown():
            log.info(f"Command Handle: Unknown Command")
            return AgvResult.Error
        
        command_handlers = {
            AgvCmd.Mode_Move : handle_mode,
            AgvCmd.Mode_Ready : handle_mode,
            AgvCmd.Mode_Search : handle_mode,
            AgvCmd.Run_Auto : handle_mode,
            AgvCmd.Run_Motor : handle_mode,
            AgvCmd.Go_To_Charge_Station : handle_mode,
            AgvCmd.Go_Away_Charge_Station : handle_mode,
            AgvCmd.Correction_Attitude : handle_mode,
            AgvCmd.Correction_Distance : handle_mode,
            AgvCmd.Shelves_Correction_Attitude : handle_mode,
            AgvCmd.Shelves_Correction_Distance : handle_mode,
            AgvCmd.Capture : handle_mode,
            AgvCmd.Shelves_Capture : handle_mode,
            AgvCmd.Script_Start : handle_script,
            AgvCmd.Script_Loop : handle_script,
            AgvCmd.Turn_Left_90 : handle_move,
            AgvCmd.Turn_Right_90 : handle_move,
            AgvCmd.Turn_Left_180: handle_move,
            AgvCmd.Turn_Right_180: handle_move,
            AgvCmd.Tray_Stop_Turn_Left_90: handle_move,
            AgvCmd.Tray_Stop_Turn_Right_90: handle_move,
            AgvCmd.Tray_Stop_Turn_Left_180: handle_move,
            AgvCmd.Tray_Stop_Turn_Right_180: handle_move,
            AgvCmd.Tray_Turn_Left_90: handle_move,
            AgvCmd.Tray_Turn_Right_90: handle_move,
            AgvCmd.Tray_Turn_Left_180: handle_move,
            AgvCmd.Tray_Turn_Right_180: handle_move,
            AgvCmd.Correction_Tray_Down: handle_move,
            AgvCmd.Correction_Tray_Rotate: handle_move,
            AgvCmd.Tray_Line: handle_move,
            AgvCmd.Tray_Lift_Up: handle_move,
            AgvCmd.Tray_Put_Down: handle_move,
            AgvCmd.Auto_Tray_Lift_Up: handle_move,
            AgvCmd.Auto_Tray_Put_Down: handle_move,
            AgvCmd.Send_Dis_AutoRun : handle_sendautorun,
            AgvCmd.Send_Dis_MotorRun : handle_sendmotorrun,
            AgvCmd.Send_Dis_Charge : handle_sendcharge,
        }
        
        handler = command_handlers.get(cmd, handle_unknown)
        return handler(cmd, data)
        
  
    @staticmethod
    def AgvCmdHandle(index: int):
        AgvComm.__ads_list[index].Connect()
        AgvComm.__config_list[index] = AgvComm.__ads_list[index].UpdateParam()

        log = logging.getLogger("log")
        
        delay = False
        count = 0
        connect = False
        isUpdateCheckTime = False
        checkTime = time.time()
        check_bat = True
        isCharging = False
        isStopCharging = True
        scriptDone = False
        
        
        while not AgvComm.isCmdHandleTerminated:
            time.sleep(0.1)
            
            if isUpdateCheckTime:
                checkTime = time.time()
                isUpdateCheckTime = False
            
            #try:
            AgvComm.__config_list[index] = AgvComm.__ads_list[index].UpdateParam()
            
            ads = AgvComm.__ads_list[index]
            cfg = AgvComm.__config_list[index]
            
            #連線狀態
            ts = time.time() - checkTime
            if ts > 10 and cfg is None:
                isUpdateCheckTime = True
                
                ads.Connect()
                ads.UpdateParam()
                
            
            if ads.IsConnect != connect:
                if connect:
                    log.info(f"INFO: Car {ads.name} OFFLINE")
                    connect = ads.IsConnect
                else:
                    log.info(f"INFO: Car {ads.name} ONLINE")
                    connect = ads.IsConnect
            
            
            # 緊急停止
            if ts > 15 and cfg is not None and cfg.Status.Flag.IsEmergencyStop:
                isUpdateCheckTime = True
                log.info(f"INFO: Car {ads.name} Emergency Stop")
            
            # 電量
            if cfg is not None and cfg.Battery <= 20 and check_bat:
                log.info(f"INFO: Car {ads.name} Low Battery, Battery = {cfg.Battery}%")
                check_bat = False
            elif cfg is not None and cfg.Battery > 20 and not check_bat:
                check_bat = True

            if cfg is not None and not isCharging and cfg.Status.Flag.IsChargeing:
                isCharging = True
                isStopCharging = False
                log.info(f"INFO: Car {ads.name} Start Charging, Battery = {cfg.Battery}%")
            elif cfg is not None and not isStopCharging and not cfg.Status.Flag.IsChargeing:
                isCharging = False
                isStopCharging = True
                log.info(f"INFO: Car {ads.name} Stop Charging, Battery = {cfg.Battery}%")
            
            #腳本執行完畢
            if cfg is not None and not scriptDone and cfg.Status.Flag.IsScriptFinish:
                scriptDone = True
                log.info(f"INFO: Car {ads.name} Script Done")
            elif cfg is not None and not cfg.Status.Flag.IsScriptFinish:
                scriptDone = False
                
            #處理命令
            if not delay and len(ads.CtrlQueue) != 0 and not ads.IsBusy and not ads.IsCmdUsed:
                ads.IsBusy = True
                
                if len(ads.CtrlQueue) == 1:
                    delay = True
                    count = 0
                    
                func = ads.CtrlQueue.pop(0)
                try:
                    func()
                except:
                    pass
                
            elif len(ads.CtrlQueue) != 0 and ads.IsBusy and ads.IsCmdUsed and cfg.Status.Flag.IsScriptStart:
                ads.CtrlQueue.clear()
            
            if delay and not ads.IsBusy:
                count += 1
                if count >= 25:
                    delay = False
                    ads.CtrlQueue.clear()
            
# class Logger:
#     def __init__(self):
#         self.subscribers = []

#     def subscribe(self, callback):
#         """讓 UI 或其他元件訂閱 log 更新"""
#         self.subscribers.append(callback)

#     def log(self, msg):
#         """發送 log 給所有訂閱者"""
#         for cb in self.subscribers:
#             cb(msg) 
            
# if __name__ == "__main__":       
#     TARGET_NETID = "192.168.100.239.1.1"  
#     AgvComm.AddAgv("239", TARGET_NETID)
#     time.sleep(1)


#     cmd1 = CommandItem(CommandType.TrayLeft180)
#     cmd2 = CommandItem(CommandType.TrayRight90)
#     cmd3 = CommandItem(CommandType.TrayRight90)
    
#     cmdList = [cmd2, cmd1, cmd3]
    
#     res = AgvComm.Start("239", cmdList=cmdList)
#     print(res)
    
    # AgvComm.DisConnect()
