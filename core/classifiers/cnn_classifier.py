import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
from typing_extensions import override

from PIL import Image

from tqdm.notebook import tqdm

from .abstract_classifier import AbstractBarcodeClassifier
from barcodes.barcodes import Barcode, TRUE_KEY, SUBSET_KEY

ConvLayerConfig = Tuple[int, int, int, int]

DEFAULT_CONV_ARCH: Tuple[ConvLayerConfig, ...] = (
    (16, 3, 2, 1),
    (32, 3, 2, 1),
    (48, 3, 2, 1),
    (64, 3, 2, 1),
    (96, 3, 2, 1),
    (128, 3, 2, 1),
)

_WEIGHTS_FOLDER = Path('../saved_results')


def _preprocess_image(image_array: np.ndarray, resize_to: int) -> np.ndarray:
    img = Image.fromarray(image_array)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((resize_to, resize_to), Image.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr.transpose(2, 0, 1)


class MemmapDataset(torch.utils.data.Dataset):
    def __init__(self, memmap: np.ndarray, indices: List[int], labels: List[int]):
        self._memmap = memmap
        self._indices = indices
        self._labels = labels

    def __len__(self) -> int:
        return len(self._indices)

    def __getitem__(self, i: int) -> Tuple[torch.Tensor, int]:
        x = torch.from_numpy(self._memmap[self._indices[i]].copy())
        return x, self._labels[i]


class SharedImageCache:
    def __init__(self, resize_to: int):
        self._resize_to = resize_to
        self._id_to_idx: Dict[str, int] = {}
        self._memmap_path: Optional[Path] = None
        self._memmap: Optional[np.ndarray] = None
        self._n_stored = 0

    def build(self, dataset: List[Barcode], margin_rate: float) -> None:
        _WEIGHTS_FOLDER.mkdir(parents=True, exist_ok=True)
        tmp_path = _WEIGHTS_FOLDER / f"_img_cache_{id(self)}.npy"
        self._memmap_path = tmp_path
        self._memmap = np.memmap(
            tmp_path, dtype=np.float32, mode='w+',
            shape=(len(dataset), 3, self._resize_to, self._resize_to),
        )
        for barcode in tqdm(dataset, desc="Building image cache"):
            barcode.do_preprocessing(margin_rate)
            if barcode.image_array is not None:
                self._memmap[self._n_stored] = _preprocess_image(barcode.image_array, self._resize_to)
                self._id_to_idx[barcode.get_id()] = self._n_stored
                self._n_stored += 1
            barcode.do_postprocessing()
        self._memmap.flush()

    def get_indices_and_labels(
        self, dataset: List[Barcode], type_to_class: Dict
    ) -> Tuple[List[int], List[int]]:
        indices, labels = [], []
        for barcode in dataset:
            label = type_to_class.get(barcode.marked_up_type)
            if label is None:
                continue
            idx = self._id_to_idx.get(barcode.get_id())
            if idx is None:
                continue
            indices.append(idx)
            labels.append(label)
        return indices, labels

    @property
    def memmap(self) -> np.ndarray:
        return self._memmap

    def cleanup(self) -> None:
        if self._memmap is not None:
            del self._memmap
            self._memmap = None
        if self._memmap_path is not None and self._memmap_path.exists():
            self._memmap_path.unlink()

    def __enter__(self) -> 'SharedImageCache':
        return self

    def __exit__(self, *_) -> None:
        self.cleanup()


class CNNBarcodeClassifier(AbstractBarcodeClassifier):
    def __init__(self, name, solver_name, margin_rate, subsets, /, *,
                 resize_to: int = 64,
                 conv_arch: Sequence[ConvLayerConfig] = DEFAULT_CONV_ARCH,
                 use_cached_res: bool = False,
                 batched_mode: bool = False):
        super().__init__(name, solver_name, margin_rate,
                         use_cached_res=use_cached_res,
                         batched_mode=batched_mode,
                         parse_img=True)
        self._resize_to = resize_to
        self._conv_arch = tuple(conv_arch)
        self._subsets = [sorted(subset) for subset in subsets]
        self._n_classes = len(self._subsets)
        self._type_to_class = {
            tp: idx
            for idx, subset in enumerate(self._subsets)
            for tp in subset
        }
        self._model = None
        self._device = None
        self._prefetched_tensor = None

    def _preprocess_image(self, image_array: np.ndarray) -> np.ndarray:
        return _preprocess_image(image_array, self._resize_to)

    def _to_tensor(self, image_array: np.ndarray):
        return torch.tensor(self._preprocess_image(image_array)[np.newaxis], dtype=torch.float32)

    def _build_model(self):
        layers = []
        in_ch = 3
        for out_ch, ks, stride, pad in self._conv_arch:
            layers.extend([
                nn.Conv2d(in_ch, out_ch, kernel_size=ks, stride=stride, padding=pad),
                nn.ReLU(inplace=True),
            ])
            in_ch = out_ch
        return nn.Sequential(
            *layers,
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_ch, self._n_classes),
        )

    def _get_weights_path(self) -> Path:
        return _WEIGHTS_FOLDER / f"cnn_weights_{self._name}_{self._solver_name}.pt"

    @override
    def _collect_fit_info(self, _: Barcode) -> None:
        pass

    def fit(self, dataset: List[Barcode], shared_cache: Optional[SharedImageCache] = None) -> None:
        weights_path = self._get_weights_path()
        if weights_path.exists():
            tqdm.write(f"[{self._name}] loading weights from {weights_path.name}")
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self._model = self._build_model().to(self._device)
            self._model.load_state_dict(
                torch.load(weights_path, map_location=self._device, weights_only=True)
            )
            self._model.eval()
            return
        tqdm.write(f"[{self._name}] fit started (n={len(dataset)})")
        own_cache = shared_cache is None
        if own_cache:
            shared_cache = SharedImageCache(self._resize_to)
            shared_cache.build(dataset, self._margin_rate)
        tqdm.write(f"[{self._name}] collecting labels")
        indices, labels = shared_cache.get_indices_and_labels(dataset, self._type_to_class)
        tqdm.write(f"[{self._name}] {len(labels)} samples -> training")
        self._train_model(shared_cache.memmap, indices, labels)
        if own_cache:
            shared_cache.cleanup()
        _WEIGHTS_FOLDER.mkdir(parents=True, exist_ok=True)
        torch.save(self._model.state_dict(), weights_path)
        tqdm.write(f"[{self._name}] weights saved to {weights_path.name}")

    def _train_model(self, memmap: np.ndarray, indices: List[int], labels: List[int]) -> None:
        torch.manual_seed(0)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if device.type == "cuda":
            torch.cuda.manual_seed_all(0)
        self._device = device
        model = self._build_model().to(device)
        train_dataset = MemmapDataset(memmap, indices, labels)
        generator = torch.Generator()
        generator.manual_seed(0)
        loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=128, shuffle=True, num_workers=0, generator=generator,
        )
        optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
        criterion = nn.CrossEntropyLoss()
        EPOCHS = 10
        model.train()
        epoch_bar = tqdm(range(EPOCHS), desc=f"Training {self._name}")
        for _ in epoch_bar:
            total_loss = 0.0
            for bX, by in loader:
                bX, by = bX.to(device), by.to(device)
                optimizer.zero_grad()
                loss = criterion(model(bX), by)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            epoch_bar.set_postfix(loss=f"{total_loss / len(loader):.4f}")
        model.eval()
        self._model = model

    def predict(self, dataset: List[Barcode]) -> None:
        rng = enumerate(dataset) if self._batched_mode else \
            tqdm(enumerate(dataset), total=len(dataset), desc="Classifier processing")
        for i, barcode in rng:
            barcode.do_preprocessing(self._margin_rate, self._parse_img)
            self._prefetched_tensor = (
                self._to_tensor(barcode.image_array)
                if barcode.image_array is not None else None
            )
            start = time.time()
            result = self._predict_one(barcode)
            result.stats.classifier_time = time.time() - start
            self._prefetched_tensor = None
            result.do_postprocessing()
            dataset[i] = result

    @override
    def _predict_one(self, barcode: Barcode) -> Barcode:
        barcode.stats.set_classifier_key(TRUE_KEY, [barcode.marked_up_type])
        if self._model is None or self._prefetched_tensor is None:
            all_types = [tp for subset in self._subsets for tp in subset]
            barcode.possible_types = all_types
            barcode.stats.set_classifier_key(SUBSET_KEY, all_types)
            return barcode
        x = self._prefetched_tensor.to(self._device)
        with torch.no_grad():
            pred_class = self._model(x).argmax(dim=1).item()
        predicted_subset = self._subsets[pred_class]
        barcode.possible_types = list(predicted_subset)
        barcode.stats.set_classifier_key(SUBSET_KEY, predicted_subset)
        return barcode
