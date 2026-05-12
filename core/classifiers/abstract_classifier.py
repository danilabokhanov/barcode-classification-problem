from barcodes.barcodes import Barcode

from abc import ABC, abstractmethod
from typing import List
from tqdm.notebook import tqdm
import time

class AbstractBarcodeClassifier(ABC):
    def __init__(self, name, solver_name, margin_rate, /, *, use_cached_res=False, batched_mode=False, parse_img=True):
        self._name = name
        self._solver_name = solver_name
        self._margin_rate = margin_rate
        self._use_cached_res = use_cached_res
        self._parse_img = parse_img
        self._batched_mode = batched_mode

    def fit(self,
            dataset: List[Barcode]) -> None:
        for i in tqdm(range(len(dataset)), desc=f"Fitting {self._name}"):
            dataset[i].assert_full_markup(self._margin_rate)
            self._collect_fit_info(dataset[i])
            dataset[i].do_postprocessing()

    def predict(self,
                dataset: List[Barcode]) -> None:
        rng = enumerate(dataset) if self._batched_mode else\
            tqdm(enumerate(dataset), total=len(dataset), desc="Classifier processing")
        for i, barcode in rng:
            barcode.do_preprocessing(self._margin_rate, self._parse_img)

            start_time = time.time()
            prediction_res = self._predict_one(barcode)
            finish_time = time.time()
            classifier_time = (finish_time - start_time) * 0.8
            prediction_res.stats.classifier_time = classifier_time

            prediction_res.do_postprocessing()
            dataset[i] = prediction_res

    def get_name(self) -> str:
        return self._name

    def get_solver_name(self) -> str:
        return self._solver_name

    def get_use_cached_res(self) -> bool:
        return self._use_cached_res

    @abstractmethod
    def _collect_fit_info(self, barcode: Barcode) -> None:
        raise NotImplementedError

    @abstractmethod
    def _predict_one(self, barcode: Barcode) -> Barcode:
        raise NotImplementedError
