from barcodes.barcodes import Barcode
from dataclasses import dataclass
from typing import List, Callable, Tuple


@dataclass
class BarcodesDataset:
    train: list[Barcode]
    val: list[Barcode]
    test: list[Barcode]

    def filter(self, predicate: Callable[[Barcode], bool]) -> "BarcodesDataset":
        return BarcodesDataset(
            train=[b for b in self.train if predicate(b)],
            val=[b for b in self.val if predicate(b)],
            test=[b for b in self.test if predicate(b)],
        )
