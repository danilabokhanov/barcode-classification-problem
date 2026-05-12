from .abstract_solver import AbstractBarcodeSolver
from barcodes.barcodes import BarcodeType, Barcode

import zxingcpp
from abc import abstractmethod
from typing_extensions import override

class ZXingCppSolver(AbstractBarcodeSolver):
    MARKUP2ZXING_CPP = {
        BarcodeType.QR_CODE: zxingcpp.BarcodeFormat.QRCode,
        BarcodeType.DATA_MATRIX: zxingcpp.BarcodeFormat.DataMatrix,
        BarcodeType.EAN_13: zxingcpp.BarcodeFormat.EAN13,
        BarcodeType.UPC_A: zxingcpp.BarcodeFormat.UPCA,
        BarcodeType.UPC_E: zxingcpp.BarcodeFormat.UPCE,
        BarcodeType.CODE_128: zxingcpp.BarcodeFormat.Code128,
        BarcodeType.CODE_39: zxingcpp.BarcodeFormat.Code39,
        BarcodeType.EAN_8: zxingcpp.BarcodeFormat.EAN8,
        BarcodeType.ITF: zxingcpp.BarcodeFormat.ITF,
        BarcodeType.PDF_417: zxingcpp.BarcodeFormat.PDF417,
        BarcodeType.AZTEC: zxingcpp.BarcodeFormat.Aztec
    }

    ZXING_CPP2MARKUP = {
        zxingcpp.BarcodeFormat.QRCode: BarcodeType.QR_CODE,
        zxingcpp.BarcodeFormat.DataMatrix: BarcodeType.DATA_MATRIX,
        zxingcpp.BarcodeFormat.EAN13: BarcodeType.EAN_13,
        zxingcpp.BarcodeFormat.UPCA: BarcodeType.UPC_A,
        zxingcpp.BarcodeFormat.UPCE: BarcodeType.UPC_E,
        zxingcpp.BarcodeFormat.Code128: BarcodeType.CODE_128,
        zxingcpp.BarcodeFormat.Code39: BarcodeType.CODE_39,
        zxingcpp.BarcodeFormat.EAN8: BarcodeType.EAN_8,
        zxingcpp.BarcodeFormat.ITF: BarcodeType.ITF,
        zxingcpp.BarcodeFormat.PDF417: BarcodeType.PDF_417,
        zxingcpp.BarcodeFormat.Aztec: BarcodeType.AZTEC
    }

    def __init__(self, margin_rate, batched_mode):
        super().__init__("ZxingCpp", margin_rate, batched_mode)

    @staticmethod
    def create_formats_from_hints(hints):
        formats = zxingcpp.BarcodeFormats(zxingcpp.BarcodeFormat.NONE)
        for hint in hints:
            mapped_format = ZXingCppSolver.MARKUP2ZXING_CPP[hint]
            assert mapped_format is not None, f"mapping for {hint} is not specified"
            formats |= mapped_format
        return formats

    @override
    def _solve_one(self, barcode: Barcode) -> Barcode:
        formats = ZXingCppSolver.create_formats_from_hints(barcode.possible_types)
        solution = zxingcpp.read_barcode(
            barcode.image_array,
            formats=formats
        ) 
        if solution is not None:
            barcode.stats.actual_type = ZXingCppSolver.ZXING_CPP2MARKUP.get(solution.format)
            barcode.stats.actual_text = solution.text
        return barcode

    @override
    def consider_running_cleanup(self, force_cleanup=False) -> None:
        pass
