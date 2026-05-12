from .zxing_cpp_solver import ZXingCppSolver

class ZXingCppLightSolver(ZXingCppSolver):
    def __init__(self, margin_rate, batched_mode: bool = False):
        super().__init__(margin_rate, batched_mode)
        self._name = "ZxingCppLight"
