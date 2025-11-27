from enum import Enum

class AgvResult(Enum):
    OK = 1
    Error = 2
    NotConnected = 3
    InvalidMode = 4
    InvalidAgvParam = 5
    Busy = 900

class CCDType(Enum):
    Up = 50
    Down = 46
    
class AxisType(Enum):
    AxisB = 66
    AxisR = 67
    AxisL = 68
    AxisUD = 69
    AxisT = 70
    
class AgvCmd(Enum):
    #30100-30131 
    Mode_Ready = 30100
    Mode_Move = 30101
    Mode_Search = 30102
    Run_Auto = 30111
    Run_Motor = 30112
    Go_To_Charge_Station = 30113
    Go_Away_Charge_Station = 30114
    Run_Pause_To_Code = 30115
    Run_Update_To_Code = 30116
    Run_Reset_To_Code = 30117
    Correction_Distance = 30121
    Correction_Attitude = 30122
    Shelves_Correction_Distance = 30123
    Shelves_Correction_Attitude = 30124
    Capture = 30125
    Shelves_Capture = 30128


    #30200-30231
    Turn_Right_90 = 30202
    Turn_Right_180 = 30203
    Turn_Left_90 = 30204
    Turn_Left_180 = 30205
    Tray_Stop_Turn_Right_90 = 30206
    Tray_Stop_Turn_Right_180 = 30207
    Tray_Stop_Turn_Left_90 = 30208
    Tray_Stop_Turn_Left_180 = 30209
    Tray_Turn_Right_90 = 30210
    Tray_Turn_Right_180 = 30211
    Tray_Turn_Left_90 = 30212
    Tray_Turn_Left_180 = 30213
    Correction_Tray_Down = 30216
    Correction_Tray_Rotate = 30217
    Tray_Line = 30218
    Tray_Lift_Up = 30221
    Tray_Put_Down = 30222
    Auto_Tray_Lift_Up = 30223
    Auto_Tray_Put_Down = 30224


    #30300-30331
    Reset_Motor_Stop = 30300
    Reset_Error_Flag = 30301
    Reset_Cancel = 30305
    Script_Start = 30306
    Reset_Stop = 30307
    Reset_Pause = 30308
    Reset_Cont = 30309
    Script_Loop = 30310
    Reset_Loop = 30311
    Jog_Forward = 30312
    Jog_Backward = 30313
    Jog_Left = 30314
    Jog_Right = 30315
    Jog_Move_Stop = 30316
    Open_Laser_Enable = 30321
    Close_Laser_Enable = 30322
    Mode_Jog_End = 30323
    Mode_Jog_Start = 30324
    Open_Jog_Search_Enable = 30326
    Close_Jog_Search_Enable = 30327
    Red_Zone_Cont = 30330
    Red_Zone_Stop = 30331

    #30400 --  30401
    CarPause = 30400#fan 20210809
    CarContinue = 30401#fan 20210809


    #100-119 其他
    Send_ScriptList = 101
    Send_Run_Velo = 102
    Send_Run_Acce = 103
    Send_Run_Dece = 104
    Send_Run_Jerk = 105
    Send_Run_Param = 106
    Send_Dis_Charge = 109
    Send_Dis_AutoRun = 110
    Send_Dis_MotorRun = 111
    Send_Tag_Pause = 32460