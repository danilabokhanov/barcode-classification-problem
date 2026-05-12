from barcodes.barcodes import BarcodeType, Barcode

import sys
from collections import defaultdict
from sklearn.model_selection import train_test_split

class DatasetSpitter:
    RANDOM_STATE=57

    def __init__(self):
        self.barcode_inds_train: list[int] = []
        self.barcode_inds_val: list[int] = []
        self.barcode_inds_test: list[int] = []
        self.cur_map: dict[BarcodeType, list] = defaultdict(list)

    def flush_chunk(self):
        for tp, inds in self.cur_map.items():
            if len(inds) > 2:
                train_inds, test_inds = train_test_split(
                    inds,
                    test_size=0.15,
                    random_state=self.RANDOM_STATE
                )
                train_inds, val_inds = train_test_split(
                    train_inds,
                    test_size=0.1765,
                    random_state=self.RANDOM_STATE
                )
            else:
                train_inds = inds[:-1]
                val_inds = []
                test_inds = inds[-1:]
            print(
                f"split chunk with type '{tp}': total sz {len(inds)}, "
                f"train sz {len(train_inds)}, val sz {len(val_inds)}, "
                f"test sz {len(test_inds)}"
            )
            self.barcode_inds_train.extend(train_inds)
            self.barcode_inds_val.extend(val_inds)
            self.barcode_inds_test.extend(test_inds)
        self.cur_map = defaultdict(list)
    
    def add_ind(self, tp: BarcodeType, ind: int):
        self.cur_map[tp].append(ind)
    
    def split_barcodes(self, barcodes: list[Barcode]) -> tuple[list[Barcode], list[Barcode], list[Barcode]]:
        self.flush_chunk()
        self.barcode_inds_train.sort()
        self.barcode_inds_val.sort()
        self.barcode_inds_test.sort()
        barcodes_train: list[Barcode] = [barcodes[i] for i in self.barcode_inds_train]
        barcodes_val: list[Barcode] = [barcodes[i] for i in self.barcode_inds_val]
        barcodes_test: list[Barcode] = [barcodes[i] for i in self.barcode_inds_test]
        return barcodes_train, barcodes_val, barcodes_test
