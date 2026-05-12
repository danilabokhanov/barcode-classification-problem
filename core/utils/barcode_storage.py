from barcodes.barcodes import BarcodeType, Barcode
from classifiers.abstract_classifier import AbstractBarcodeClassifier
from solvers.abstract_solver import AbstractBarcodeSolver
from utils.barcodes_dataset import BarcodesDataset
from utils.mode import is_testing_mode
from typing import List, Tuple
from pathlib import Path
import pickle
import os

STORAGE_FOLDER = Path('../saved_results')

class BarcodeStorage:
    @staticmethod
    def save(
        barcodes: BarcodesDataset | list[Barcode],
        filepath: Path
    ) -> None:
        with filepath.open("wb") as f:
            pickle.dump(barcodes, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filepath: Path) -> Tuple[BarcodesDataset | list[Barcode], bool]:
        try:
            with filepath.open("rb") as f:
                return pickle.load(f), True
        except Exception as e:
            return [], False

    @staticmethod
    def get_filepath_by_pipeline(classifier: AbstractBarcodeClassifier) -> Path:
        os.makedirs(STORAGE_FOLDER, exist_ok=True)
        return STORAGE_FOLDER /\
            f"dump_pipeline_{classifier.get_name()}_{classifier.get_solver_name()}.pickle"

    @staticmethod
    def get_filepath_by_dataset_name(dataset_name: str) -> Path:
        os.makedirs(STORAGE_FOLDER, exist_ok=True)
        return STORAGE_FOLDER / f"dump_dataset_{dataset_name}{'_light' if is_testing_mode() else ''}.pickle"
