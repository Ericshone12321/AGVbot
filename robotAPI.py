from fastapi import FastAPI
from pydantic import BaseModel
from AGV_SDK.WCSFunction import WCSFunction
import instructions

wcs = WCSFunction()
app = FastAPI(title="AGV 控制 API", version="1.0.0")
robot = instructions.AGV("240", wcs)

# ====== SwitchBot MAC Address ======
UP_BOT_MAC = "F2:B2:05:86:32:6C"
DOWN_BOT_MAC = "F2:B2:00:86:3A:6C"

class ApiResult(BaseModel):
    ok: bool
    message: str = ""


class MoveRequest(BaseModel):
    target: str  # 例如 "010020"

@app.post("/AGV/MoveTo", response_model=ApiResult, summary="移動到指定位置")
async def MoveTo(req: MoveRequest):
    try:
        await instructions.MoveToTarget(robot, str(req.target))
        return ApiResult(ok=True, message=f"AGV 已移動到 {req.target}")

    except Exception as e:
        return ApiResult(ok=False, message=f"移動失敗: {e}")

@app.post("/turnTray/left90", response_model=ApiResult, summary="控制轉盤左轉90度")
async def turn_tray_left90():
    try:
        await instructions.turn_tray_left90(robot)
        return ApiResult(ok=True, message="轉盤左轉90度成功")

    except Exception as e:
        return ApiResult(ok=False, message=f"轉盤左轉90度失敗: {e}")

@app.post("/turnTray/right90", response_model=ApiResult, summary="控制轉盤右轉90度")
async def turn_tray_right90():
    try:
        await instructions.turn_tray_right90(robot)
        return ApiResult(ok=True, message="轉盤右轉90度成功")

    except Exception as e:
        return ApiResult(ok=False, message=f"轉盤右轉90度失敗: {e}")

@app.post("/bed/up", response_model=ApiResult, summary="控制病床上升")
async def bed_up():
    try:
        await instructions.press_bot(UP_BOT_MAC)
        return ApiResult(ok=True, message="病床上升成功")

    except Exception as e:
        return ApiResult(ok=False, message=f"病床上升失敗: {e}")

@app.post("/bed/down", response_model=ApiResult, summary="控制病床下降")
async def bed_down():
    try:
        await instructions.press_bot(DOWN_BOT_MAC)
        return ApiResult(ok=True, message="病床下降成功")

    except Exception as e:
        return ApiResult(ok=False, message=f"病床下降失敗: {e}")

# @app.post("/AGV/HomeToP1ToHome", response_model=ApiResult, summary="HomeToP1ToHome")
# async def HomeToP1ToHome():
#     await instructions.HomeToP1ToHome(robot)
#     return ApiResult(ok=True, message="AGV 已完成 HomeToP1ToHome")

# @app.post("/AGV/HomeToP2", response_model=ApiResult, summary="HomeToP2")
# async def HomeToP2():
#     await instructions.HomeToP2(robot)
#     return ApiResult(ok=True, message="AGV 已啟動 HomeToP2")

# @app.post("/AGV/P2ToP3", response_model=ApiResult, summary="P2ToP3")
# async def P2ToP3():
#     await instructions.P2ToP3(robot)
#     return ApiResult(ok=True, message="AGV 已啟動 P2ToP3")

# @app.post("/AGV/P3ToP4", response_model=ApiResult, summary="P3ToP4")
# async def P3ToP4():
#     await instructions.P3ToP4(robot)
#     return ApiResult(ok=True, message="AGV 已啟動 P3ToP4")

# @app.post("/AGV/P4ToHome", response_model=ApiResult, summary="P4ToHome")
# async def P4ToHome():
#     await instructions.P4ToHome(robot)
#     return ApiResult(ok=True, message="AGV 已啟動 P4ToHome")

