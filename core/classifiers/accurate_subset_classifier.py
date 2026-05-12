from .abstract_classifier import AbstractBarcodeClassifier
from barcodes.barcodes import Barcode, TRUE_KEY, MULTI_KEY_WITH_GR_TRUTH

from abc import abstractmethod
from typing_extensions import override

class AccurateSubsetClassifier(AbstractBarcodeClassifier):
    def __init__(self, name, solver_name, margin_rate, subsets, /, *, use_cached_res=False, batched_mode=False):
        super().__init__(name, solver_name, margin_rate, use_cached_res=use_cached_res, batched_mode=batched_mode, parse_img=False)
        self._subsets = [sorted(subset) for subset in subsets]

    @override
    def _collect_fit_info(self, barcode: Barcode) -> None:
        pass

    @override
    def _predict_one(self, barcode: Barcode) -> Barcode:
        barcode.stats.set_classifier_key(TRUE_KEY, [barcode.marked_up_type])
        for subset in self._subsets:
            if barcode.marked_up_type in subset:
                barcode.possible_types.extend(subset)
                ordered_subset = [barcode.marked_up_type] +\
                    [tp for tp in subset if tp != barcode.marked_up_type]
                barcode.stats.set_classifier_key(MULTI_KEY_WITH_GR_TRUTH, ordered_subset)
                return barcode
        assert False, f"subset not found for type '{barocde.margin_rate}' and solver '{self._solver_name}'"
