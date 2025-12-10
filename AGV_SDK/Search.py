from dataclasses import dataclass #@dataclass用法基本同C的struct，用來快速定義資料容器類別
import os
import json
from .AgvComm import *
from .AgvCmdItem import *

@dataclass
class Point:
    #存x, y座標，A*的父節點和F值
    x: int
    y: int 
    last_x: int = None
    last_y: int = None
    f: float = 0.0

def Read_map_config() -> dict:
    #讀入json檔案(禁行區+貨架+單行道資訊)
    filepath = os.path.join(os.getcwd(), 'map_config.json')
    with open(filepath, 'r', encoding = 'utf-8') as f:
        data = json.load(f)

    nogo = [Point(p['x'], p['y']) for p in data.get('nogo', [])]
    shelves = [Point(p['x'], p['y']) for p in data.get('shelves', [])]
    oneway = []
    for seg in data.get('oneway', []):
        pts = [Point(p['x'], p['y']) for p in seg.get('points', [])]
        oneway.append({'direction': seg.get('direction'), 'points': pts})
    return {'nogo': nogo, 'shelves': shelves, 'oneway': oneway}

def G_cost(consider: Point, now: Point, zones: dict) -> int:
    #單行道成本
    #""" 
    dx = consider.x - now.x
    dy = consider.y - now.y

    if dx > 0 and dy == 0: move_dir = 'xPos' #往x+1(向下走)
    elif dx < 0 and dy == 0: move_dir = 'xNeg' #往x-1(向上走)
    elif dx == 0 and dy > 0: move_dir = 'yPos' #往y+1(向右走)
    elif dx == 0 and dy < 0: move_dir = 'yNeg' #往y-1(向左走)
    else: return 1

    # 檢查當前考慮的點是否屬於單行道
    limited = set() #每個點的方向限制可能有多個，先全部記錄
    for seg in zones.get('oneway', []):
        if any(p.x == consider.x and p.y == consider.y for p in seg['points']):
            limited.add(seg['direction'])        

    if limited:
        return 1 if move_dir in limited else 10000 #有限制但方向不符重罰
    #"""
    #正常道路
    return 1 #給機械所只要留這一行

def H_cost(point: Point, TargetPoint: Point) -> int:
    #曼哈頓距離公式|x1 - x2| + |y1 - y2|
    return abs(point.x - TargetPoint.x) + abs(point.y - TargetPoint.y)

def CrossProduct(lat0, lng0, lat1, lng1, lat2, lng2) -> bool:
    #ccw = 0:三點在同一直線上，沒有轉彎; ccw != 0:三點不共線，發生轉彎
    ccw = (lng0 - lng1) * lat2 + (lat1 - lat0) * lng2 + lat0 * lng1 - lat1 * lng0
    return ccw != 0

def Find_father(close: list[Point], current: Point, result_list: list[Point]) -> None:
    #追溯父節點、路徑
    result_list.insert(0, current) #把當前節點插到路徑最前面
    father = next((p for p in close if p.x == current.last_x and p.y == current.last_y), None)
    
    #如果父節點存在，就遞迴呼叫自己，繼續往上找，直到回到起點
    if father:
        Find_father(close, father, result_list)    

def Turn_cost(close: list[Point], ConsiderPoint: Point) -> int:
    result = []
    Find_father(close, ConsiderPoint, result)
    if len(result) > 2:
        if CrossProduct(result[-1].x, result[-1].y, 
                        result[-2].x, result[-2].y, 
                        result[-3].x, result[-3].y):
            return 3 #轉彎成本 = 3
    return 0 #直走，則轉彎成本 = 0

#將路徑轉為腳本
def ToScript(initial_ang: int, route_list: list[Point]) -> list[CommandItem]:
    commands: list[CommandItem] = []
    ang = initial_ang + 90
    if ang > 360: 
        ang -= 360

    #遍歷路徑
    for i in range(1, len(route_list)):
        #看前後點的差值來判斷方向
        dx = route_list[i].x - route_list[i - 1].x
        dy = route_list[i].y - route_list[i - 1].y

        if ang < 45 or ang > 315: #0度 (車頭朝左)
            if dx == 0 and dy < 0: #車頭朝左->往左走 #直接直走
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1))
            elif dx < 0 and dy == 0: #車頭朝左->往上走
                commands.append(CommandItem(CommandType.TurnRight90ByTrayStop)) #先右轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 90
            elif dx == 0 and dy > 0: #車頭朝左->往右走
                commands.append(CommandItem(CommandType.TurnRight180ByTrayStop)) #先右轉180
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 180
            else: #車頭朝左->往下走
                commands.append(CommandItem(CommandType.TurnLeft90ByTrayStop)) #先左轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 270        
        elif 45 < ang < 135: #90度 (車頭朝上)
            if dx < 0 and dy == 0: #車頭朝上->往上走 #直接直走
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1))
            elif dx == 0 and dy < 0: #車頭朝上->往左走
                commands.append(CommandItem(CommandType.TurnLeft90ByTrayStop)) #先左轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 0
            elif dx == 0 and dy > 0: #車頭朝上->往右走
                commands.append(CommandItem(CommandType.TurnRight90ByTrayStop)) #先右轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 180
            else: #車頭朝上->往下走
                commands.append(CommandItem(CommandType.TurnRight180ByTrayStop)) #先右轉180
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 270      
        elif ang > 135 and ang < 225: #180度 (車頭朝右)
            if dx == 0 and dy > 0: #車頭朝右->往右走 #直接直走
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1))
            elif dx < 0 and dy == 0: #車頭朝右->往上走
                commands.append(CommandItem(CommandType.TurnLeft90ByTrayStop)) #先左轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 90
            elif dx > 0 and dy == 0: #車頭朝右->往下走
                commands.append(CommandItem(CommandType.TurnRight90ByTrayStop)) #先右轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 270
            else: #車頭朝右->往左走
                commands.append(CommandItem(CommandType.TurnRight180ByTrayStop)) #先左轉180
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 0      
        else:
            #270度 (車頭朝下)
            if dx > 0 and dy == 0: #車頭朝下->往下走 #直接直走
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1))
            elif dx == 0 and dy < 0: #車頭朝下->往左走
                commands.append(CommandItem(CommandType.TurnRight90ByTrayStop)) #先右轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 0
            elif dx == 0 and dy > 0: #車頭朝下->往右走
                commands.append(CommandItem(CommandType.TurnLeft90ByTrayStop)) #先左轉90
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 180
            else: #車頭朝下->往上走
                commands.append(CommandItem(CommandType.TurnLeft180ByTrayStop)) #先左轉180
                commands.append(CommandItem(CommandType.GoForwardInMeter + 1)) #再直走
                ang = 90 
    # 合併連續直走命令
    merged: list[CommandItem] = []
    for cmd in commands:
        if merged and cmd.Type == CommandType.GoForwardInMeter and merged[-1].Type == CommandType.GoForwardInMeter:
            merged[-1].Parameter += cmd.Parameter
        else:
            merged.append(cmd)
    return merged

#A* 演算法規畫路徑
def Path_Search(AgvName: str, start: Point, target: Point, zones: dict, angle: int):
    nogo = zones.get('nogo', [])
    shelves = zones.get('shelves', [])

    cfg = AgvComm.GetAgvCfg(AgvName)
    if cfg is None: #AGV尚未Add或名稱錯誤
        return f"NO found {AgvName}", [] 
    
    #阻擋集合：紅區+貨架格
    #備註：不能讓AGV在貨架底下穿過，只有搬運的必要時刻才能走到貨架下搬出來到非貨架格
    blocked = {(p.x, p.y) for p in nogo}|{(p.x, p.y) for p in shelves}

    #起點/終點是否在貨架格上
    start_is_shelf = any(p.x == start.x and p.y == start.y for p in shelves)
    target_is_shelf = any(p.x == target.x and p.y == target.y for p in shelves)
    #若在貨架格，則開放那一格可以走
    if start_is_shelf:
        blocked.discard((start.x, start.y))
    if target_is_shelf:
        blocked.discard((target.x, target.y))

    if((start.x, start.y) == (target.x, target.y) or 
       any(p.x == target.x and p.y == target.y for p in nogo) or 
       any(p.x == start.x and p.y == start.y for p in nogo)):
        return "無可用路徑3: 起始點與目的點相同 或 起始點或目的點屬於紅區", []  

    close = [start] #已處理的點
    open_list = [] #待處理的點
    now = start #目前點，初始為起點

    #搜尋主迴圈
    while True:
        neighbors = [Point(now.x+1, now.y), Point(now.x, now.y+1), Point(now.x-1, now.y), Point(now.x, now.y-1)]
        for nb in neighbors:
            if(1 <= nb.x <= 3 and 1 <= nb.y <= 3 and
               (nb.x, nb.y) not in blocked and
               not any(p.x == nb.x and p.y == nb.y for p in close) and
               not any(p.x == nb.x and p.y == nb.y for p in open_list)):
                #紀錄父節點(前一個是誰)
                nb.last_x, nb.last_y = now.x, now.y
                step_cost = G_cost(nb, now, zones)
                if step_cost >= 10000:
                    continue

                #F=到終點的距離+單行道成本+轉彎成本+父節點的成本
                #now.f：累積成本(從起點走到目前點的成本)
                nb.f = H_cost(nb, target) + G_cost(nb, now, zones) + Turn_cost(close, nb) + (now.f if now != start else 0)
                open_list.append(nb)

        #終止條件：open已空，close過大
        if not open_list or len(close) > 1000:
            break

        #選擇最佳下一步
        #找到open中F最小的點，加入close，從open中刪除
        open_list.sort(key = lambda p: p.f) #將open中的點按F值由小到大排序
        now = open_list.pop(0) #pop出list中最小的點(剛剛已經排序好了)
        close.append(now)

        #終止條件：找到目標終點
        if (now.x == target.x and now.y == target.y):
            break 
    
    if 1 < len(close) < 1000 and now.x == target.x and now.y == target.y:
        result = []
        Find_father(close, now, result)

        if result:
            try:
                script_cmds = ToScript(angle, result)
                route_str = "".join(f"{c.Type.name}, {c.Parameter}\n" for c in script_cmds)
                return route_str, script_cmds
            except Exception as e:
                return str(e), []
        else:
            return "無用路徑1: 路徑計算錯誤", []
    else:
        return "無用路徑2: 目前條件無可用路徑", []

""" if __name__ == '__main__':
    AgvComm.AddAgv('217', '192.168.100.217.1.1') #新增AGV並啟動通訊
    cfg = AgvComm.GetAgvCfg('217')

    #等待連線
    time.sleep(0.5)

    #讀取地圖設定、起訖點 
    zones = Read_map_config()
    start = Point(8,2) #弄UI輸入
    target = Point(10,2) #弄UI輸入

    #呼叫路徑規劃
    route, cmds = Path_Search('217', start, target, zones, 90)
    print(f"AGV: {'217'}")
    print(route) """