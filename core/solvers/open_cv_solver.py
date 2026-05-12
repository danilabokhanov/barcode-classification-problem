from .abstract_solver import AbstractBarcodeSolver
from barcodes.barcodes import BarcodeType, Barcode

from typing_extensions import override
import cv2
import numpy as np


class OpenCVSolver(AbstractBarcodeSolver):
    MARKUP2OPENCV = {
        BarcodeType.QR_CODE: "QR_CODE",
        BarcodeType.EAN_13: "EAN_13",
        BarcodeType.EAN_8: "EAN_8",
        BarcodeType.UPC_A: "UPC_A",
        BarcodeType.UPC_E: "UPC_E",
        BarcodeType.CODE_128: "CODE_128",
        BarcodeType.CODE_39: "CODE_39",
        BarcodeType.ITF: "ITF",
    }

    OPENCV2MARKUP = {v: k for k, v in MARKUP2OPENCV.items()}

    def __init__(self, margin_rate, batched_mode):
        super().__init__("OpenCv", margin_rate, batched_mode)

        self.qr_detector = cv2.QRCodeDetector()
        self.barcode_detector = cv2.barcode.BarcodeDetector()

    def _is_qr_only(self, possible_types):
        return (len(possible_types) == 1 and 
                possible_types[0] == BarcodeType.QR_CODE)

    def _contains_qr(self, possible_types):
        return BarcodeType.QR_CODE in possible_types

    def _try_qr_detector(self, image):
        try:
            data, bbox, straight_qrcode = self.qr_detector.detectAndDecode(image)
            if data:
                return data, BarcodeType.QR_CODE
        except Exception as e:
            print(f"failed to parse qr: {e}")
        return None, None

    def _try_barcode_detector(self, image):
        try:
            ok, decoded_info, decoded_type, corners = self.barcode_detector.detectAndDecodeWithType(image)
            if ok and decoded_info is not None and len(decoded_info) > 0:
                text = decoded_info[0]
                if text:
                    if decoded_type is not None and len(decoded_type) > 0:
                        barcode_type = self.OPENCV2MARKUP.get(decoded_type[0])
                        return text, barcode_type

                    return text, None
        except Exception as e:
            print(f"failed to parse common code: {e}")
        return None, None

    @override
    def _solve_one(self, barcode: Barcode) -> Barcode:
        image = barcode.image_array
        if self._is_qr_only(barcode.possible_types):
            text, barcode_type = self._try_qr_detector(image)
        elif self._contains_qr(barcode.possible_types):
            text, barcode_type = self._try_qr_detector(image)
            if text is None:
                text, barcode_type = self._try_barcode_detector(image)
        else:
            text, barcode_type = self._try_barcode_detector(image)
        barcode.stats.actual_text = text
        barcode.stats.actual_type = barcode_type
        return barcode

    @override
    def consider_running_cleanup(self, force_cleanup=False) -> None:
        pass
