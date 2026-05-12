from .abstract_classifier import AbstractBarcodeClassifier
from barcodes.barcodes import Barcode, TRUE_KEY

from abc import abstractmethod
from typing_extensions import override

class DummyClassifier(AbstractBarcodeClassifier):
    def __init__(self, name, solver_name, margin_rate, /, *, use_cached_res=False, batched_mode=False):
        super().__init__(name, solver_name, margin_rate, use_cached_res=use_cached_res, batched_mode=batched_mode, parse_img=False)

    @override
    def _collect_fit_info(self, barcode: Barcode) -> None:
        pass

    @override
    def _predict_one(self, barcode: Barcode) -> Barcode:
        barcode.stats.set_classifier_key(TRUE_KEY, [barcode.marked_up_type])
        return barcode
