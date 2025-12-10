from AGV_SDK.WCSFunction import WCSFunction
import time
import asyncio
from bleak import BleakClient

IsMoving = False
CurrentPosition = None
IsScriptFinish = False
ScriptStarted = False
IsBusy = False

# ====== SwitchBot BLE UUID ======
SERVICE_UUID = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
CHAR_UUID    = "cba20002-224d-11e6-9fb8-0002a5d5c51b"



async def status_worker(wcs):
    global IsMoving, CurrentPosition, IsScriptFinish, IsBusy
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
            IsBusy = status.Status.AxisM.Busy

            print("Position:", CurrentPosition)
            print("IsMoving:", IsMoving)
            print("IsScriptFinish:", IsScriptFinish)
            print("IsBusy:", IsBusy)
            print("direction:", wcs.get_car_status("240").Location.A)
            print("---------------------------------------------")

        except Exception as e:
            print("[ERROR] status_worker 發生錯誤：", repr(e))

        await asyncio.sleep(0.2)


async def wait_until_stop(timeout=30, stable_count=20):
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


async def run_move_to_target(target, robot, timeout=40):
    start = time.time()
    
    # step 1：先等上一段動作完成（Idle = Busy=False）
    while IsBusy:
        if time.time() - start > timeout:
            print("Timeout：上一段動作仍 Busy")
        await asyncio.sleep(0.1)

    if(int(target) == robot.wcs.get_car_status("240").Attitude.Code):
        print("已在目標點，無需移動")
        return True

    print(f"開始 move_to_target → {target}")
    #如果在小圈內就走出來
    if(robot.wcs.get_car_status("240").Attitude.Code == 210110):
        if(robot.wcs.get_car_status("240").Location.A == 0):
            await robot.turn_left90()
            await robot.run(140)
            time.sleep(3)
            await robot.turn_right90()
            await robot.wait_pos(210130)
            await robot.run(600)
            await robot.turn_right90()
            await robot.wait_pos(20010)
            robot.wcs.move_to_target("240", target)

    #小圈進入點
    elif(target == "020010"):
        if(robot.wcs.get_car_status("240").Attitude.Code == 30010):
            if(robot.wcs.get_car_status("240").Location.A == 18000):
                await robot.turn_left180()
                await robot.wait_pos(30010)
            if(robot.wcs.get_car_status("240").Location.A == 0):
                await robot.run(500)
                await robot.turn_right90()
                await robot.run(140)
                await robot.turn_left180()
                await robot.wait_pos(210110)
                print("move_to_target 完成")
                return True
        else:
            robot.wcs.move_to_target("240", target)
            await robot.wait_pos(int(target))
            if(robot.wcs.get_car_status("240").Location.A == 0):
                await robot.turn_left180()
            if(robot.wcs.get_car_status("240").Location.A == 18000):
                await robot.run(600)
                await robot.turn_left90()
                await robot.run(140)
                time.sleep(3)
                await robot.turn_left90()
                await robot.wait_pos(210110)
                print("move_to_target 完成")
                return True
    else:
        robot.wcs.move_to_target("240", target)

    # step 2：等待動作開始（Busy=True）
    while not IsBusy:
        if time.time() - start > timeout:
            print("Timeout：move_to_target 沒有開始")
        await asyncio.sleep(0.1)

    # step 3：等待動作完成（Busy=False）
    while IsBusy:
        if time.time() - start > timeout:
            print("Timeout：move_to_target 執行時間過長")
        await asyncio.sleep(1)
    await wait_until_position(int(target))

    print("move_to_target 完成")
    return True

async def wait_until_position(target_code, timeout=30):
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

# ====== SwitchBot ======
async def press_bot(mac: str):
    try:
        async with BleakClient(mac) as client:
            if not client.is_connected:
                return False, "連線 SwitchBot 失敗"

            # 取得特徵值
            char = client.services.get_service(SERVICE_UUID).get_characteristic(CHAR_UUID)

            # 按下
            await client.write_gatt_char(char, bytearray([0x57, 0x01, 0x01]))

            return True, "成功按壓 SwitchBot"
    except Exception as e:
        return False, f"錯誤: {e}"

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
    
    async def _wait_busy_clear(self, timeout=10):
        start = time.time()
        while IsBusy:
            if time.time() - start > timeout:
                raise RuntimeError("Busy 一直為 True，無法發送指令")
            await asyncio.sleep(0.1)

    async def run(self, distance):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.motor_run(self.id, distance)
        return self

    async def turn_right90(self):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.turn_right90(self.id)
        return self

    async def turn_left90(self):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.turn_left90(self.id)
        return self

    async def turn_left180(self):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.turn_left180(self.id)
        return self
    
    async def tray_turn_left90(self):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.tray_left90(self.id)
        return self
    
    async def tray_turn_right90(self):
        await wait_until_stop()
        await self._wait_busy_clear()
        self.wcs.tray_right90(self.id)
        return self

    async def target_script(self, target, robot):
        await wait_until_stop()
        await self._wait_busy_clear()
        await run_move_to_target(target, robot)
        return self

async def MoveToTarget(robot, target):
    worker = asyncio.create_task(status_worker(robot.wcs))
    await asyncio.sleep(0.5)

    await robot.target_script(target, robot)

    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")


async def turn_tray_left90(robot):
    worker = asyncio.create_task(status_worker(robot.wcs))
    await asyncio.sleep(0.5)

    await robot.tray_turn_left90()

    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")

async def turn_tray_right90(robot):
    worker = asyncio.create_task(status_worker(robot.wcs))
    await asyncio.sleep(0.5)

    await robot.tray_turn_right90()

    print("全部腳本完成，準備停止監控")
    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("監控成功結束")