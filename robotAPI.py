from fastapi import FastAPI
from pydantic import BaseModel
from AGV_SDK.WCSFunction import WCSFunction
import instructions

wcs = WCSFunction()
app = FastAPI(title="AGV 控制 API", version="1.0.0")
robot = instructions.AGV("240", wcs)

class ApiResult(BaseModel):
    ok: bool
    message: str = ""
    data: dict | None = None


@app.post("/AGV/HomeToP1ToHome", response_model=ApiResult, summary="HomeToP1ToHome")
async def HomeToP1ToHome():
    await instructions.HomeToP1ToHome(robot)
    return ApiResult(ok=True, message="AGV 已完成 HomeToP1ToHome")

@app.post("/AGV/HomeToP2", response_model=ApiResult, summary="HomeToP2")
async def HomeToP2():
    await instructions.HomeToP2(robot)
    return ApiResult(ok=True, message="AGV 已啟動 HomeToP2")

@app.post("/AGV/P2ToP3", response_model=ApiResult, summary="P2ToP3")
async def P2ToP3():
    await instructions.P2ToP3(robot)
    return ApiResult(ok=True, message="AGV 已啟動 P2ToP3")

@app.post("/AGV/P3ToP4", response_model=ApiResult, summary="P3ToP4")
async def P3ToP4():
    await instructions.P3ToP4(robot)
    return ApiResult(ok=True, message="AGV 已啟動 P3ToP4")

@app.post("/AGV/P4ToHome", response_model=ApiResult, summary="P4ToHome")
async def P4ToHome():
    await instructions.P4ToHome(robot)
    return ApiResult(ok=True, message="AGV 已啟動 P4ToHome")



