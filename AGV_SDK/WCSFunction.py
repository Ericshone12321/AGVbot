from .AgvComm import *
from .AgvCmdItem import *
from .AgvLogging import setup_logging
from .Search import Path_Search, Read_map_config, Point
import threading
from dataclasses import dataclass
from typing import Optional

@dataclass
class iCar:
    carID: str
    config : Optional[AgvConfig] = None

class WCSFunction():
    icar_list = []
    def __init__(self) -> None:
        
        AgvComm.AddAgv("240", "192.168.100.240.1.1")
        WCSFunction.icar_list.append(iCar("240"))

        # AgvComm.AddAgv("238", "192.168.100.238.1.1")
        # WCSFunction.icar_list.append(iCar("238"))

        for icar in WCSFunction.icar_list:
            t = threading.Thread(target=self.update_status, args=(icar, ), daemon=True)
            t.start()
        
        setup_logging()
        self.log = logging.getLogger("log")

    def update_status(self, car:iCar) -> None:
        while True:
            time.sleep(0.2) #200毫秒更新一次

            cfg = AgvComm.GetAgvCfg(car.carID)
            
            if cfg is not None:
                car.config = cfg

    def get_car_status(self, carID) -> AgvConfig:
        '''得到AGV所有狀態資料'''
        return next((c.config for c in WCSFunction.icar_list if c.carID == carID), None)

    def run_robot_script(self, carID:str, task_name:str) -> str:
        '''執行指定的腳本'''
        cmd_list : list[CommandItem] = []
        cfg = AgvComm.GetAgvCfg(carID)
        code = cfg.Attitude.Code
        print("Task Name:", task_name)

        if task_name == "HomeToP2":
            if code == 10010:
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+1))
        elif task_name == "P2ToP3":
            if code == 10020:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+1))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
        elif task_name == "P3ToP4":
            if code == 30010:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
        elif task_name == "P4ToHome":
            if code == 30030:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))
        elif task_name == "AllRoute":
            if code == 10010:
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+1))
        
            if code == 10020:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+1))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
        
            if code == 30010:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnRight90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
        
            if code == 30030:
                cmd_list.append(CommandItem(CommandType.TurnLeft180ByTrayStop))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))
                cmd_list.append(CommandItem(CommandType.GoForwardInMeter+2))
                cmd_list.append(CommandItem(CommandType.TurnLeft90))

        if len(cmd_list) != 0:
            AgvComm.Start(carID, cmd_list)
            return "success"
        else:
            return "failed"

    def move_to_target(self, carID:str, target:str) -> str:
        '''命令AGV移動到指定點'''
        cfg = AgvComm.GetAgvCfg(carID)
        start = Point(int(cfg.Attitude.Code/10000), int(cfg.Attitude.Code%1000/10))
        
        end = Point(int(int(target)/10000), int(int(target)%1000/10))
        zones = Read_map_config()
        angle = cfg.Attitude.A

        route, cmds = Path_Search(carID, start, end, zones, angle)

        print(route)
        
        AgvComm.Start(carID, cmds)
        return route
        
    def auto_run(self, carID:str, distance:int):
        '''AGV前進指定距離，距離單位為毫米(mm)，每1000mm為一單位，不可為負值'''
        AgvComm.AutoRun(carID, distance)

    def motor_run(self, carID:str, distance:int):
        '''AGV前進指定距離，距離單位為毫米(mm)'''
        AgvComm.MotorRun(carID, distance)

    def turn_left90(self, carID:str):
        '''AGV左轉90度(轉盤不動)'''
        AgvComm.TrayStopTurnLeft90(carID)

    def turn_left180(self, carID:str):
        '''AGV左轉180度(轉盤不動)'''
        AgvComm.TrayStopTurnLeft180(carID)

    def turn_right90(self, carID:str):
        '''AGV右轉90度(轉盤不動)'''
        AgvComm.TrayStopTurnRight90(carID)
    
    def turn_right180(self, carID:str):
        '''AGV右轉180度(轉盤不動)'''
        AgvComm.TrayStopTurnRight180(carID)
    
    def tray_left90(self, carID:str):
        '''轉盤左轉90度'''
        AgvComm.TrayTurnLeft90(carID)

    def tray_left180(self, carID:str):
        '''轉盤左轉180度'''
        AgvComm.TrayTurnLeft180(carID)
    
    def tray_right90(self, carID:str):
        '''轉盤右轉90度'''
        AgvComm.TrayTurnRight90(carID)
    
    def tray_right180(self, carID:str):
        '''轉盤右轉180度'''
        AgvComm.TrayTurnRight180(carID)