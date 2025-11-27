from AGV_SDK.WCSFunction import WCSFunction
import time
import asyncio

IsMoving = False
CurrentPosition = None
IsScriptFinish = False
ScriptStarted = False

def show(wcs):
    print(wcs.get_car_status("240"))

async def status_worker(wcs):
    global IsMoving, CurrentPosition, IsScriptFinish
    while True:
        try:
            status = wcs.get_car_status("240")

            if status is None:
                print("[WARN] get_car_status 回傳 None，可能尚未連線或暫時斷線")
                # 不更新狀態，等下一輪
                await asyncio.sleep(0.5)
                continue

            IsMoving = status.Status.Flag.IsMoving
            CurrentPosition = status.Attitude.Code
            IsScriptFinish = status.Status.Flag.IsScriptFinish

            print("Position:", CurrentPosition)
            print("IsMoving:", IsMoving)
            print("IsScriptFinish:", IsScriptFinish)

        except Exception as e:
            print("[ERROR] status_worker 發生錯誤：", repr(e))

        await asyncio.sleep(0.2)


async def wait_until_stop(timeout=10, stable_count=10):
    start = time.time()
    stable = 0

    while True:
        if not IsMoving:
            stable += 1
        else:
            stable = 0

        if stable >= stable_count:
            return True

        if time.time() - start > timeout:
            raise RuntimeError("AGV 停止不穩定或卡住，wait_until_stop 超時")

        await asyncio.sleep(0.1)


async def run_script(wcs, script_name, timeout=40):
    global ScriptStarted
    start = time.time()

    if not ScriptStarted:
        print(f"[首次] 執行腳本: {script_name}")
        wcs.run_robot_script("240", script_name)
        ScriptStarted = True
    else:
        while not IsScriptFinish:
            if time.time() - start > timeout:
                print("Timeout：上一條 Script 尚未完成")
                return False
            await asyncio.sleep(0.1)

        print(f"執行腳本: {script_name}")
        wcs.run_robot_script("240", script_name)

    # 等開始執行 (IsScriptFinish False)
    while IsScriptFinish:
        if time.time() - start > timeout:
            print("Timeout：Script 未開始")
            return False
        await asyncio.sleep(0.1)

    # 等執行完成 (IsScriptFinish True)
    while not IsScriptFinish:
        if time.time() - start > timeout:
            print("Timeout：Script 未完成")
            return False
        await asyncio.sleep(0.1)

    print("Script 完成")
    return True


async def wait_until_position(target_code, timeout=10):
    await wait_until_stop()

    start = None  # 還沒開始計時

    while True:
        # 第一次拿到有效的位置時才開始計時
        if CurrentPosition is not None and start is None:
            start = time.time()

        if CurrentPosition == target_code:
            print(f"到達座標 {target_code}")
            return True

        if start is not None and (time.time() - start > timeout):
            print(f"等待座標 {target_code} 超時！目前位置 {CurrentPosition}")
            return False

        await asyncio.sleep(0.1)


class AGV:
    def __init__(self, id, wcs):
        self.id = id
        self.wcs = wcs

    async def wait_pos(self, pos):
        ok = await wait_until_position(pos)
        if not ok:
            raise RuntimeError(f"AGV 未到達座標 {pos}")
        return self

    async def wait_stop(self):
        await wait_until_stop()
        return self

    async def run(self, distance):
        await wait_until_stop()
        self.wcs.motor_run(self.id, distance)
        return self

    async def turn_left90(self):
        await wait_until_stop()
        self.wcs.turn_left90(self.id)
        return self

    async def turn_right90(self):
        await wait_until_stop()
        self.wcs.turn_right90(self.id)
        return self

    async def turn_left180(self):
        await wait_until_stop()
        self.wcs.turn_left180(self.id)
        return self

    async def script(self, name):
        await run_script(self.wcs, name)
        return self

async def HomeToP1ToHome(robot):
    # 啟動狀態監控
    worker = asyncio.create_task(status_worker(robot.wcs))

    await asyncio.sleep(0.5)

    await robot.wait_pos(10010)
    await robot.run(1600)
    await robot.turn_left90()

    await robot.wait_pos(210130)
    await robot.run(140)
    await robot.turn_left180()

    await robot.wait_pos(210110)
    await robot.run(140)
    await robot.turn_right90()

    await robot.wait_pos(210130)
    await robot.run(1600)
    await robot.turn_left90()
    await robot.turn_right90()

    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")

async def HomeToP2(robot):
    # 啟動狀態監控
    worker = asyncio.create_task(status_worker(robot.wcs))

    await asyncio.sleep(0.5)

    await robot.wait_pos(10010)
    await robot.script("HomeToP2")
    
    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")

async def P2ToP3(robot):
    
    # 啟動狀態監控
    worker = asyncio.create_task(status_worker(robot.wcs))

    await asyncio.sleep(0.5)

    await robot.wait_pos(10020)
    await robot.script("P2ToP3")
    
    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")

async def P3ToP4(robot):
    
    # 啟動狀態監控
    worker = asyncio.create_task(status_worker(robot.wcs))

    await asyncio.sleep(0.5)

    await robot.wait_pos(30010)
    await robot.script("P3ToP4")
    
    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")

async def P4ToHome(robot):
    
    # 啟動狀態監控
    worker = asyncio.create_task(status_worker(robot.wcs))

    await asyncio.sleep(0.5)

    await robot.wait_pos(30030)
    await robot.script("P4ToHome")
    
    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")