from dataclasses import dataclass, field
from datetime import timedelta
from typing import Tuple, Optional, List, Dict
from numpy.typing import NDArray
from PIL import Image, ImageOps
from pathlib import Path
from enum import Enum

import numpy as np
import sys

TRUE_KEY = "true_symbology"
MULTI_KEY = "multi_key"
MULTI_KEY_WITH_GR_TRUTH = "add_symbs_with_gr_tr"
DEFAULT_KEY = "default"
DEFAULT_VALUE = "Default"
SUBSET_KEY = "subset"

class LastImageStorage:
    image_path: str = ""
    image = None

@dataclass
class Point:
    x: int
    y: int

Quad = Tuple[Point, Point, Point, Point]

unmatched_types = set()

class BarcodeType(str, Enum):
    QR_CODE = "QR_CODE"
    DATA_MATRIX = "DATA_MATRIX"
    EAN_13 = "EAN_13"
    UPC_A = "UPC_A"
    UPC_E = "UPC_E"
    CODE_128 = "CODE_128"
    CODE_39 = "CODE_39"
    EAN_8 = "EAN_8"
    ITF = "ITF"
    PDF_417 = "PDF_417"
    AZTEC = "AZTEC"
    UNDEFINED = "UNDEFINED"

    @classmethod
    def from_string(cls, value: str) -> "BarcodeType":
        try:
            value = value.upper()
            if value in ["QR_CODE", "QR", "QRCODE"]:
                return cls.QR_CODE
            if value in ["DATA_MATRIX", "DATAMATRIX"]:
                return cls.DATA_MATRIX
            if value in ["EAN_13", "EAN13"]:
                return cls.EAN_13
            if value in ["UPC_A", "UPCA"]:
                return cls.UPC_A
            if value in ["UPC_E", "UPCE"]:
                return cls.UPC_E
            if value in ["CODE_128", "C128", "CODE128"]:
                return cls.CODE_128
            if value in ["CODE_39", "C39", "CODE39"]:
                return cls.CODE_39
            if value in ["EAN_8", "EAN8"]:
                return cls.EAN_8
            if value in ["ITF", "INTERLEAVED2OF5"]:
                return cls.ITF
            if value in ["PDF_417", "PDF417"]:
                return cls.PDF_417
            if value in ["AZTEC", "AZTECCODE"] :
                return cls.AZTEC
            unmatched_types.add(value)
            return cls.UNDEFINED
        except ValueError:
            allowed = ", ".join([t.value for t in cls])
            raise ValueError(
                f"unknown barcode type '{value}'. "
                f"allowed types: {allowed}"
            )

PRETTY_PRINT_MAP = {
    BarcodeType.QR_CODE: "QR Code",
    BarcodeType.DATA_MATRIX: "DataMatrix",
    BarcodeType.EAN_13: "EAN-13",
    BarcodeType.UPC_A: "UPC-A",
    BarcodeType.UPC_E: "UPC-E",
    BarcodeType.CODE_128: "Code 128",
    BarcodeType.CODE_39: "Code 39",
    BarcodeType.EAN_8: "EAN-8",
    BarcodeType.ITF: "ITF",
    BarcodeType.PDF_417: "PDF417",
    BarcodeType.AZTEC: "Aztec",
    BarcodeType.UNDEFINED: "Undefined"
}

@dataclass
class StatEntry:
    classifier_keys: Dict[str, str] = field(default_factory=lambda: {DEFAULT_KEY: DEFAULT_VALUE})
    classifier_time: float = 0
    expected_type: Optional[BarcodeType] = None
    actual_type: Optional[BarcodeType] = None
    expected_text: Optional[str] = None
    actual_text: Optional[str] = None
    solver_time: float = 0

    def set_classifier_key(self, name, barcode_types: list[BarcodeType], *, tag: str = "") -> None:
        pieces_to_join = []
        if tag:
            pieces_to_join.append(tag)
        pieces_to_join.extend(tp for tp in barcode_types)
        key = "/".join(pieces_to_join)
        self.classifier_keys[name] = key 


@dataclass
class Barcode:
    label: Optional[str] = None
    index: Optional[int] = None
    image_path: Optional[Path] = None
    image_array: Optional[NDArray] = None
    quad: Optional[Quad] = None
    marked_up_type: Optional[BarcodeType] = None
    marked_up_text: Optional[str] = None
    possible_types: List[BarcodeType] = field(default_factory=list)
    stats: StatEntry = field(default_factory=StatEntry)

    def do_preprocessing(self, margin_rate, parse_img=True):
        assert self.quad is not None
        if self.image_array is not None:
            return
        assert self.image_path is not None
        if not parse_img:
            return
        try:
            if LastImageStorage.image_path == self.image_path:
                image = LastImageStorage.image
            else:
                with Image.open(self.image_path) as image_raw:
                    LastImageStorage.image = image = ImageOps.exif_transpose(image_raw)
                LastImageStorage.image_path = self.image_path

            xs = [point[0] for point in self.quad]
            ys = [point[1] for point in self.quad]
            min_xs = min(xs)
            max_xs = max(xs)
            width = max_xs - min_xs
            min_ys = min(ys)
            max_ys = max(ys)
            height = max_ys - min_ys
            assert width > 0 and height > 0
            min_x = max(0, int(min(xs) - width * margin_rate))
            min_y = max(0, int(min(ys) - height * margin_rate))
            max_x = min(image.width, int(max(xs) + width * margin_rate) + 1)
            max_y = min(image.height, int(max(ys) + height * margin_rate) + 1)
            image_cropped = image.crop((min_x, min_y, max_x, max_y))
            self.image_array = np.array(image_cropped)
            assert self.image_array.ndim == 2 or self.image_array.ndim == 3
            assert self.image_array.dtype == np.uint8
            assert self.image_array.flags["C_CONTIGUOUS"]
        except Exception as e:
            print(f"image preprocessing failed with image {self.image_path}", file=sys.stderr)
            raise

    def do_postprocessing(self):
        self.image_array = None

    def assert_full_markup(self, margin_rate):
        self.do_postprocessing()
        assert self.marked_up_type is not None
        assert self.marked_up_text is not None

    def get_id(self) -> 'str':
        return f'{self.label}_{self.index}'
    
    def is_solved(self):
        if self.stats.actual_type is None or self.stats.expected_type is None\
            or self.stats.actual_text is None or self.stats.expected_text is None:
            return False
        if (self.stats.actual_type == BarcodeType.UPC_A and self.stats.expected_type == BarcodeType.EAN_13):
            return self.stats.actual_text == self.stats.expected_text[1:]
        if (self.stats.actual_type == BarcodeType.UPC_A and self.stats.expected_type == BarcodeType.UPC_E):
            return self.stats.actual_text == self.stats.expected_text
        return self.stats.actual_type == self.stats.expected_type\
            and self.stats.actual_text == self.stats.expected_text
