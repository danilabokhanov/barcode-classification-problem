from barcodes.barcodes import BarcodeType

import inspect
import sys


ALL_TYPES = {
    "OpenCv": {BarcodeType.EAN_8, BarcodeType.EAN_13, BarcodeType.UPC_A, BarcodeType.QR_CODE},
    "Zbar": {
        BarcodeType.CODE_39, BarcodeType.CODE_128, BarcodeType.EAN_8,
        BarcodeType.EAN_13, BarcodeType.UPC_A, BarcodeType.UPC_E, BarcodeType.ITF,
        BarcodeType.QR_CODE
    },
    "ZxingCpp": {
        BarcodeType.CODE_39, BarcodeType.CODE_128, BarcodeType.EAN_8,
        BarcodeType.EAN_13, BarcodeType.UPC_A, BarcodeType.UPC_E, BarcodeType.ITF,
        BarcodeType.QR_CODE, BarcodeType.DATA_MATRIX, BarcodeType.AZTEC, BarcodeType.PDF_417
    },
    "ZxingJava": {
        BarcodeType.CODE_39, BarcodeType.CODE_128, BarcodeType.EAN_8,
        BarcodeType.EAN_13, BarcodeType.UPC_A, BarcodeType.UPC_E, BarcodeType.ITF,
        BarcodeType.QR_CODE, BarcodeType.DATA_MATRIX, BarcodeType.AZTEC, BarcodeType.PDF_417
    }
}


def validate_decomposition(
    dec,
    name,
    *,
    require_full_cover=True,
):
    for solver_name, all_types in ALL_TYPES.items():
        if solver_name not in dec:
            continue
        subsets = [set(group) for group in dec[solver_name]]

        seen = set()
        for group in subsets:
            intersection = seen & group
            if intersection:
                raise ValueError(
                    "decomposition is not disjoint. "
                    f"Intersection: {intersection} for {name}"
                )
            seen |= group

        if require_full_cover:
            if seen != all_types:
                missing = all_types - seen
                extra = seen - all_types
                raise ValueError(
                    f"decomposition mismatch for {name}.\nMissing: {missing}\nExtra: {extra}"
                )


def validate_all_decompositions(module=None):
    if module is None:
        module = sys.modules[__name__]

    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("get_") and name.endswith("_decomposition"):
            dec = obj()

            if not isinstance(dec, dict):
                raise TypeError(f"{name} must return dict")

            validate_decomposition(dec, name, require_full_cover=True)

    print("all decompositions are valid.")

def get_all_partitions_2_11_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.QR_CODE,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_2_43_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.QR_CODE,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_46_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.QR_CODE,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_67_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_2_75_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_2_99_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_100_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_101_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.ITF,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_107_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_108_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_109_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_110_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_115_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_116_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.PDF_417,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_123_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_2_124_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_579_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_3_621_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_3_645_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_3_648_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_3_654_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_3_672_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_3_681_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_690_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_699_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_708_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_810_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_3_837_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_864_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_3_873_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_882_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_3_888_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_3_891_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_3_942_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_642_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_643_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_4_659_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.ITF,
            ],
        ]
    }


def get_all_partitions_4_671_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_673_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_4_751_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_4_765_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_825_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_4_839_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_924_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_928_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_4_929_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_931_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_933_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_4_987_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.ITF,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_1084_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_4_1103_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1106_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_4_1108_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1259_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1466_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1468_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1474_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1476_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1498_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1642_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
        ]
    }


def get_all_partitions_4_1658_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_4_1690_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_179_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_5_198_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_263_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
        ]
    }


def get_all_partitions_5_415_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_420_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_460_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_461_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_590_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_594_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_5_609_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_614_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_5_618_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_5_637_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_652_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_672_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_5_677_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_680_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_5_731_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_5_741_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
        ]
    }


def get_all_partitions_5_890_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
        ]
    }


def get_all_partitions_6_9_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_29_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_31_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_44_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_45_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_47_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_48_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_49_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_83_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_84_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_85_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
        ]
    }


def get_all_partitions_6_104_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_105_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_6_220_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_221_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_234_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_240_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_6_246_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_7_2_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_7_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_7_8_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_7_9_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_11_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_12_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_13_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_14_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_7_15_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.ITF,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_16_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_17_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
                BarcodeType.ITF,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_24_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }


def get_all_partitions_7_25_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
                BarcodeType.QR_CODE,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
        ]
    }


def get_all_partitions_8_0_decomposition():
    return {
        "ZxingCpp": [
            [
                BarcodeType.AZTEC,
            ],
            [
                BarcodeType.CODE_128,
            ],
            [
                BarcodeType.CODE_39,
            ],
            [
                BarcodeType.DATA_MATRIX,
            ],
            [
                BarcodeType.EAN_13,
                BarcodeType.EAN_8,
                BarcodeType.UPC_A,
                BarcodeType.UPC_E,
            ],
            [
                BarcodeType.ITF,
            ],
            [
                BarcodeType.PDF_417,
            ],
            [
                BarcodeType.QR_CODE,
            ],
        ]
    }
