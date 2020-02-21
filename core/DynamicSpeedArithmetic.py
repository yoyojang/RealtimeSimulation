# 根据损耗时间输出下一次的速度
class DynamicSpeedArithmetic:
    def __init__(self, realtime, simutime):
        self.realtime = realtime
        self.simutime = simutime

    def main(self):
        speed = self.simutime / self.realtime
        return speed