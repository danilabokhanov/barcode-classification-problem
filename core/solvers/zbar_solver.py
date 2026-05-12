from .abstract_solver import AbstractBarcodeSolver
from barcodes.barcodes import BarcodeType, Barcode

from typing_extensions import override
import ctypes
import numpy as np
import os


_libzbar = ctypes.CDLL("libzbar.so")

zbar_image_t = ctypes.c_void_p
zbar_image_scanner_t = ctypes.c_void_p
zbar_symbol_t = ctypes.c_void_p

SUPPORTED_ZBAR = [
    BarcodeType.QR_CODE,
    BarcodeType.UPC_A, BarcodeType.UPC_E,
    BarcodeType.EAN_13, BarcodeType.EAN_8,
    BarcodeType.CODE_128, BarcodeType.CODE_39,
    BarcodeType.ITF
]

ZBAR_NONE = 0
ZBAR_QRCODE = 64
ZBAR_EAN13 = 13
ZBAR_EAN8 = 8
ZBAR_UPCA = 12
ZBAR_UPCE = 9
ZBAR_CODE128 = 128
ZBAR_CODE39 = 39
ZBAR_ITF = 25
ZBAR_PDF417 = 57
ZBAR_DATAMATRIX = 71

ZBAR_CFG_ENABLE = 0
ZBAR_CFG_UNCERTAINTY = 64

_libzbar.zbar_image_scanner_create.restype = zbar_image_scanner_t

_libzbar.zbar_image_scanner_destroy.argtypes = [zbar_image_scanner_t]

_libzbar.zbar_image_scanner_set_config.argtypes = [
    zbar_image_scanner_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]

_libzbar.zbar_image_create.restype = zbar_image_t

_libzbar.zbar_image_destroy.argtypes = [zbar_image_t]

_libzbar.zbar_image_set_format.argtypes = [zbar_image_t, ctypes.c_uint32]

_libzbar.zbar_image_set_size.argtypes = [zbar_image_t, ctypes.c_uint, ctypes.c_uint]

_libzbar.zbar_image_set_data.argtypes = [
    zbar_image_t,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.c_void_p,
]

_libzbar.zbar_scan_image.argtypes = [zbar_image_scanner_t, zbar_image_t]
_libzbar.zbar_scan_image.restype = ctypes.c_int

_libzbar.zbar_image_first_symbol.restype = zbar_symbol_t
_libzbar.zbar_image_first_symbol.argtypes = [zbar_image_t]

_libzbar.zbar_symbol_next.restype = zbar_symbol_t
_libzbar.zbar_symbol_next.argtypes = [zbar_symbol_t]

_libzbar.zbar_symbol_get_type.restype = ctypes.c_int
_libzbar.zbar_symbol_get_type.argtypes = [zbar_symbol_t]

_libzbar.zbar_symbol_get_data.restype = ctypes.c_char_p
_libzbar.zbar_symbol_get_data.argtypes = [zbar_symbol_t]


class ZBarSolver(AbstractBarcodeSolver):

    MARKUP2ZBAR = {
        BarcodeType.QR_CODE: ZBAR_QRCODE,
        BarcodeType.DATA_MATRIX: ZBAR_DATAMATRIX,
        BarcodeType.EAN_13: ZBAR_EAN13,
        BarcodeType.EAN_8: ZBAR_EAN8,
        BarcodeType.UPC_A: ZBAR_UPCA,
        BarcodeType.UPC_E: ZBAR_UPCE,
        BarcodeType.CODE_128: ZBAR_CODE128,
        BarcodeType.CODE_39: ZBAR_CODE39,
        BarcodeType.ITF: ZBAR_ITF,
        BarcodeType.PDF_417: ZBAR_PDF417,
    }

    ZBAR2MARKUP = {v: k for k, v in MARKUP2ZBAR.items()}

    def __init__(self, margin_rate, batched_mode):
        super().__init__("Zbar", margin_rate, batched_mode)

    @override
    def _solve_one(self, barcode: Barcode) -> Barcode:
        img = barcode.image_array
        if img.ndim == 3:
            img = (
                0.299 * img[..., 0] +
                0.587 * img[..., 1] +
                0.114 * img[..., 2]
            ).astype(np.uint8)

        height, width = img.shape

        scanner = _libzbar.zbar_image_scanner_create()

        _libzbar.zbar_image_scanner_set_config(scanner, ZBAR_NONE, ZBAR_CFG_ENABLE, 0)

        for tp in barcode.possible_types:
            zbar_sym = self.MARKUP2ZBAR.get(tp)
            if zbar_sym is not None:
                _libzbar.zbar_image_scanner_set_config(scanner, zbar_sym, ZBAR_CFG_ENABLE, 1)
                if zbar_sym == ZBAR_UPCA:
                    _libzbar.zbar_image_scanner_set_config(scanner, ZBAR_EAN13, ZBAR_CFG_ENABLE, 1)

        image = _libzbar.zbar_image_create()
        _libzbar.zbar_image_set_format(image, 0x30303859)
        _libzbar.zbar_image_set_size(image, width, height)

        buf = img.ctypes.data_as(ctypes.c_void_p)
        _libzbar.zbar_image_set_data(image, buf, img.nbytes, None)

        n = _libzbar.zbar_scan_image(scanner, image)
        if n > 0:
            sym = _libzbar.zbar_image_first_symbol(image)
            if sym:
                sym_type = _libzbar.zbar_symbol_get_type(sym)
                data = _libzbar.zbar_symbol_get_data(sym)

                barcode.stats.actual_type = self.ZBAR2MARKUP.get(sym_type)
                barcode.stats.actual_text = data.decode("utf-8", errors="replace")

        _libzbar.zbar_image_destroy(image)
        _libzbar.zbar_image_scanner_destroy(scanner)

        return barcode

    @override
    def consider_running_cleanup(self, force_cleanup=False) -> None:
        pass
