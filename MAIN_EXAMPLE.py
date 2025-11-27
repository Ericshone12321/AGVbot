from AGV_SDK.WCSFunction import WCSFunction, iCar
import time
import instructions



if __name__ == "__main__":
    wcs = WCSFunction()
    time.sleep(1)
    cfg = wcs.get_car_status("240")
    # print("cfg", cfg)
    print("Attitude:", cfg.Attitude.Code)
    # print("Battery:", cfg.Battery)
    # location = cfg.Location
    # shelves = cfg.Shelves
    print("AxisM.Busy:", cfg.Status.AxisM.Busy)
    print("AxisB.Busy:", cfg.Status.AxisB.Busy)
    print("AxisR.Busy:", cfg.Status.AxisR.Busy)
    print("AxisL.Busy:", cfg.Status.AxisL.Busy)
    print("AxisUD.Busy:", cfg.Status.AxisUD.Busy)
    print("AxisT.Busy:", cfg.Status.AxisT.Busy)
    wcs.move_to_target("240", "010030")
    print("AxisM.Busy:", cfg.Status.AxisM.Busy)
    print("AxisB.Busy:", cfg.Status.AxisB.Busy)
    print("AxisR.Busy:", cfg.Status.AxisR.Busy)
    print("AxisL.Busy:", cfg.Status.AxisL.Busy)
    print("AxisUD.Busy:", cfg.Status.AxisUD.Busy)
    print("AxisT.Busy:", cfg.Status.AxisT.Busy)
