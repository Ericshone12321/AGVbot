from AGV_SDK.WCSFunction import WCSFunction
import time
import threading

stop_event = threading.Event()
IsMoving = False
CurrentPosition = None
IsScriptFinish = False
ScriptStarted = False

def status_worker():
    global IsMoving, CurrentPosition, IsScriptFinish
    while not stop_event.is_set():
        time.sleep(0.2)
        status = wcs.get_car_status("240")

        IsMoving = status.Status.Flag.IsMoving
        CurrentPosition = status.Attitude.Code
        IsScriptFinish = status.Status.Flag.IsScriptFinish
        print("Position:", CurrentPosition)
        print("IsMoving:", IsMoving)
        print("IsScriptFinish:", IsScriptFinish)

def wait_until_stop(timeout=10, stable_count=10):
    """
    等待直到 AGV 完全穩定停止
    stable_count：需要連續幾次 IsMoving=False 才算真的停
    """
    start = time.time()
    stable = 0

    while True:
        if not IsMoving:
            stable += 1
        else:
            stable = 0   # 只要動過一次就重新計算

        # 已經穩定 N 次 → 真正停止
        if stable >= stable_count:
            return True

        # 超時
        if time.time() - start > timeout:
            print("Timeout：AGV 停止不穩定或卡住")
            return False

        time.sleep(0.1)


def auto_action(func, *args):
    wait_until_stop()
    print(f"執行動作: {func.__name__}")
    func(*args)
    time.sleep(0.5)

def run_script(func, *args, timeout=30):
    global ScriptStarted
    start = time.time()

    # 第一次執行 Script
    if not ScriptStarted:
        print(f"[首次] 執行腳本: {args}")
        func(*args)
        ScriptStarted = True

    else:
        # 等上一個 Script Idle
        while not IsScriptFinish:  
            if time.time() - start > timeout:
                print("Timeout：上一條 Script 未完成")
                return False
            time.sleep(0.1)

        print(f"執行腳本: {args}")
        func(*args)

    # 等 Script 開始執行
    while IsScriptFinish:
        if time.time() - start > timeout:
            print("Timeout：Script 未開始執行")
            return False
        time.sleep(0.1)

        # 等 Script 執行完
    while not IsScriptFinish:
        if time.time() - start > timeout:
            print("Timeout：Script 執行未完成")
            return False
        time.sleep(0.1)

    print("Script 完成")
    return True


def wait_until_position(target_code, timeout=10):
    wait_until_stop()
    start = time.time()
    while True:
        if CurrentPosition == target_code:
            print(f"到達座標 {target_code}")
            return True
        
        if time.time() - start > timeout:
            print(f"等待座標 {target_code} 超時！目前位置 {CurrentPosition}")
            return False

        time.sleep(0.1)

if __name__ == "__main__":
    wcs = WCSFunction()

    status_thread = threading.Thread(target=status_worker, daemon=True)
    status_thread.start()

    time.sleep(0.5)

    # HomeToP1ToHome
    if wait_until_position(10010):
        auto_action(wcs.motor_run, "240", 1560)
        auto_action(wcs.turn_left90, "240")

    if wait_until_position(210130):
        auto_action(wcs.motor_run, "240", 140)
        auto_action(wcs.turn_left180, "240")

    if wait_until_position(210110):
        auto_action(wcs.motor_run, "240", 140)
        auto_action(wcs.turn_right90, "240")

    if wait_until_position(210130):
        auto_action(wcs.motor_run, "240", 1650)
        auto_action(wcs.turn_left90, "240")
        auto_action(wcs.turn_right90, "240")

    wait_until_stop()
    run_script(wcs.run_robot_script, "240", "HomeToP2")

    run_script(wcs.run_robot_script, "240", "P2ToP3")

    run_script(wcs.run_robot_script, "240", "P3ToP4")

    run_script(wcs.run_robot_script, "240", "P4ToHome")

    input("按 Enter 結束狀態監聽 thread...")
    stop_event.set()
    status_thread.join()
    print("Thread 已停止")
