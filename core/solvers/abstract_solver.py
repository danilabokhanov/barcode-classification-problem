from barcodes.barcodes import Barcode

from abc import ABC, abstractmethod
from typing import List
from tqdm.notebook import tqdm
import time

class AbstractBarcodeSolver(ABC):
    def __init__(self, name, margin_rate, batched_mode=False):
        self._name = name
        self._margin_rate = margin_rate
        self._batched_mode = batched_mode

    def solve(self,
                dataset: List[Barcode]) -> None:
        rng = range(len(dataset)) if self._batched_mode else tqdm(range(len(dataset)), desc="Solver processing")
        for i in rng:
            barcode = dataset[i]
            barcode.do_preprocessing(self._margin_rate)

            start_time = time.time()
            solution = self._solve_one(barcode)
            solution.stats.expected_type = barcode.marked_up_type
            solution.stats.expected_text = barcode.marked_up_text
            finish_time = time.time()
            solver_time = finish_time - start_time
            solution.stats.solver_time = solver_time

            solution.do_postprocessing()
            dataset[i] = solution
            self.consider_running_cleanup()
        if not self._batched_mode:
            self.consider_running_cleanup(force_cleanup=True)

    @abstractmethod
    def _solve_one(self, barcode: Barcode) -> Barcode:
        raise NotImplementedError

    @abstractmethod
    def consider_running_cleanup(self, force_cleanup=False):
        raise NotImplemented

    def get_name(self):
        return self._name
