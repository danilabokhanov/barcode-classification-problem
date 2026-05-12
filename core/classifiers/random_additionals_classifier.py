from .abstract_classifier import AbstractBarcodeClassifier
from barcodes.barcodes import BarcodeType, Barcode, TRUE_KEY, MULTI_KEY, MULTI_KEY_WITH_GR_TRUTH

from random import Random
import hashlib
from abc import abstractmethod
from typing_extensions import override

class RandomAdditionalsClassifier(AbstractBarcodeClassifier):
    def __init__(
        self, name, solver_name, margin_rate, /, *, addinional_types_num=None, use_cached_res=False, batched_mode=False):
        assert addinional_types_num is None or addinional_types_num + 1 <= len(BarcodeType)
        super().__init__(name, solver_name, margin_rate, use_cached_res=use_cached_res, batched_mode=batched_mode, parse_img=False)
        self._addinional_types_num = addinional_types_num

    @override
    def _collect_fit_info(self, barcode: Barcode) -> None:
        pass

    def get_additional_options(self, barcode: Barcode) -> Barcode:
        addinional_options = []
        if self._solver_name == "OpenCv":
            for barcode_type in [BarcodeType.QR_CODE, BarcodeType.EAN_8, BarcodeType.EAN_13, BarcodeType.UPC_A]:
                if barcode_type != barcode.marked_up_type:
                    addinional_options.append(barcode_type)
            return addinional_options
        for barcode_type in BarcodeType:
            if barcode_type not in [BarcodeType.UNDEFINED, barcode.marked_up_type]:
                if self._solver_name in ["ZxingCpp", "ZxingJava"]:
                    addinional_options.append(barcode_type)
                elif self._solver_name == "Zbar":
                    if barcode_type not in [BarcodeType.AZTEC, BarcodeType.DATA_MATRIX, BarcodeType.PDF_417]:
                        addinional_options.append(barcode_type)
                else:
                    assert False, f"unknown solver name '{self._solver_name}'"
        return addinional_options

    def _get_ranked_additional_options(self, barcode: Barcode):
        addinional_options = self.get_additional_options(barcode)
        seed_input = f"{self._solver_name}|{barcode.get_id()}|{barcode.marked_up_type}"
        seed_hex = hashlib.md5(seed_input.encode("utf-8")).hexdigest()
        seed = int(seed_hex, 16)
        rng = Random(seed)
        ranked_options = addinional_options[:]
        rng.shuffle(ranked_options)
        return ranked_options

    @override
    def _predict_one(self, barcode: Barcode) -> Barcode:
        ranked_options = self._get_ranked_additional_options(barcode)
        if self._addinional_types_num is not None:
            addinional_types = ranked_options[:self._addinional_types_num]
        else:
            addinional_types = [opt for idx, opt in enumerate(ranked_options) if idx % 2 == 0]
        addinional_types.sort()
        barcode.possible_types.append(barcode.marked_up_type)
        barcode.possible_types.extend(addinional_types)
        barcode.stats.set_classifier_key(TRUE_KEY, [barcode.marked_up_type])
        if self._addinional_types_num is not None:
            barcode.stats.set_classifier_key(MULTI_KEY, addinional_types)
            barcode.stats.set_classifier_key(MULTI_KEY_WITH_GR_TRUTH, [barcode.marked_up_type] + addinional_types)
        return barcode

    def get_addinional_types_num(self):
        return self._addinional_types_num
