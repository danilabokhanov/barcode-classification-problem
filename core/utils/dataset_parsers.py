from barcodes.barcodes import BarcodeType, Barcode
from utils.barcode_storage import BarcodeStorage
from utils.data_splitter import DatasetSpitter
from utils.barcodes_dataset import BarcodesDataset
from utils.mode import is_testing_mode
from PIL import Image, ImageOps

from typing import List, Callable
from pathlib import Path
from tqdm.notebook import tqdm
from dataclasses import dataclass
import json
import sys
import random
import base64

YOLO_BARCODE_DATASET_DIR = "../yolo-barcode"
BARBER_DATASET_DIR = "../BarBeR-Dataset"
SBD_DIR = "../sbd"
SE_DMTX_SYN_DIR = "../se-dmtx-syn-1000"

def parse_yolo_barcode_dataset(dir_raw: str) -> tuple[list[Barcode], list[Barcode], list[Barcode]]:
    MAX_IMAGE_ID = 15 if is_testing_mode() else 1855
    se_dataset_dir = Path(dir_raw)
    res: List[Barcode] = []
    dataset_spitter = DatasetSpitter()
    for i in tqdm(range(MAX_IMAGE_ID), desc="Yolo barcode dataset parsing"):
        image_path = se_dataset_dir / "images" / f"IMG_{i}.png"
        markup_path = se_dataset_dir / "markup" / f"IMG_{i}.json"
        if not image_path.exists() or not markup_path.exists():
            continue

        with open(markup_path, 'r', encoding='utf-8') as f:
            markup_data = json.load(f)
            for barcode_index, barcode_info in enumerate(markup_data.get("props", {}).values()):
                barcode = Barcode()
                barcode.label = f"IMG_{i}.png"
                barcode.index = barcode_index
                barcode.image_path = image_path
                barcode.marked_up_type = BarcodeType.from_string(barcode_info["symbology"])
                if barcode.marked_up_type == BarcodeType.UNDEFINED:
                    continue
                barcode.marked_up_text = barcode_info["value"]
                barcode.quad = barcode_info["quad"]
                dataset_spitter.add_ind(barcode.marked_up_type, len(res))
                res.append(barcode)
    return dataset_spitter.split_barcodes(res)


def parse_barber_dataset(dir_raw: str) -> tuple[list[Barcode], list[Barcode], list[Barcode]]:
    barber_dataset_dir = Path(dir_raw)
    mapping_dir = barber_dataset_dir / "Annotations" / "VIA"
    images_dir = barber_dataset_dir / "dataset" / "images" 
    res: List[Barcode] = []
    dataset_spitter = DatasetSpitter()
    mapping_files_cnt = 0
    for mapping_file in mapping_dir.glob("*.json"):
        if is_testing_mode() and mapping_files_cnt >= 2:
            break
        mapping_files_cnt += 1
        with mapping_file.open("r", encoding="utf-8") as f:
            mapping = json.load(f)
        images_metadata = mapping["_via_img_metadata"]
        for full_image_name, image_metadata in images_metadata.items():
            image_file = image_metadata["filename"]
            image_path = images_dir / image_file
            try:
                with Image.open(image_path) as image_raw:
                    image = ImageOps.exif_transpose(image_raw)
            except:
                print("corrupted or missing mage was skipped:", image_file, file=sys.stderr)
                continue
            regions = image_metadata["regions"]
            for barcode_index, region in enumerate(regions):
                barcode = Barcode()
                barcode.label = full_image_name
                barcode.index = barcode_index
                barcode.image_path = image_path
                region_attributes = region["region_attributes"]
                barcode.marked_up_type = BarcodeType.from_string(region_attributes["Type"])
                if barcode.marked_up_type == BarcodeType.UNDEFINED:
                    continue
                barcode.marked_up_text = region_attributes["String"]
                shape_attributes = region["shape_attributes"]
                xs = shape_attributes.get("all_points_x")
                ys = shape_attributes.get("all_points_y")
                assert xs is not None and ys is not None and\
                        len(xs) == len(ys) and len(ys) >= 4, (
                    "Invalid bounding-box point set. "
                    f"image_path: {image_path}, xs: {xs}, ys: {ys}"
                )
                barcode.quad = [point for point in zip(xs, ys)]
                dataset_spitter.add_ind(barcode.marked_up_type, len(res))
                res.append(barcode)
        dataset_spitter.flush_chunk()
    assert mapping_files_cnt > 0
    return dataset_spitter.split_barcodes(res)


def parse_sbd(dir_raw: str)  -> tuple[list[Barcode], list[Barcode], list[Barcode]]:
    CHUNKS_COUNT = 5
    IMAGES_COUNT = 10 if is_testing_mode() else 1400
    sbd_dir = Path(dir_raw)
    res: List[Barcode] = []
    dataset_spitter = DatasetSpitter()
    for chunk_id in range(CHUNKS_COUNT):
        markup_file_path = sbd_dir / f"roi_chunk{chunk_id}_masks" / "all_bboxes.json"
        with markup_file_path.open("r", encoding="utf-8") as f:
            markup_json = json.load(f)
        for image_index in tqdm(range(IMAGES_COUNT), desc=f"sbd chunk{chunk_id} parsing"):
            image_regions = markup_json[f"img_{image_index}"]
            for barcode_index, image_region in enumerate(image_regions):
                barcode = Barcode()
                barcode.label = f"{chunk_id}_roi{image_index}.png"
                barcode.index = barcode_index
                barcode.image_path = sbd_dir / f"roi_chunk{chunk_id}_im" / f"roi{image_index}.png"
                barcode.marked_up_type = BarcodeType.from_string(image_region["type"])
                if barcode.marked_up_type == BarcodeType.EAN_13:
                    continue
                assert barcode.marked_up_type is not None,\
                    f"couldn't bind sbd type {barcode.marked_up_type} to any value"
                barcode.marked_up_text = image_region["data"]
                bbox = image_region["box"]
                barcode.quad = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
                dataset_spitter.add_ind(barcode.marked_up_type, len(res))
                res.append(barcode)
    return dataset_spitter.split_barcodes(res)


def parse_se_dmtx_syn(dir_raw: str)  -> tuple[list[Barcode], list[Barcode], list[Barcode]]:
    IMAGES_COUNT = 100 if is_testing_mode() else 1000
    dataset_dir = Path(dir_raw)
    res: List[Barcode] = []
    dataset_spitter = DatasetSpitter()
    for image_index in tqdm(range(IMAGES_COUNT), desc="se dmtx syn dataset parsing"):
        markup_file_path = dataset_dir / "markup" / f"synth_{image_index}.png.json"
        with markup_file_path.open("r", encoding="utf-8") as f:
            markup_json = json.load(f)
        barcode_json = markup_json["props"]["barcode"]
        barcode = Barcode()
        barcode.label = f"synth_{image_index}.png"
        barcode.index = 0
        barcode.image_path = dataset_dir / 'images' / f"synth_{image_index}.png"
        assert barcode_json["symbology"] == "DATA_MATRIX"
        barcode.marked_up_type = BarcodeType.from_string(barcode_json["symbology"])
        assert barcode.marked_up_type is not None
        barcode.marked_up_text = base64.b64decode(barcode_json["value"]).decode()
        barcode.quad = barcode_json["quad"]
        dataset_spitter.add_ind(barcode.marked_up_type, len(res))
        res.append(barcode)
    return dataset_spitter.split_barcodes(res)


def merge_datasets(train: List[List[Barcode]], val: List[List[Barcode]], test: List[List[Barcode]]) -> List[Barcode]:
    assert len(train) == len(val) == len(test)
    res_train: List[Barcode] = []
    for dataset in train:
        res_train.extend(dataset)
    random.shuffle(res_train)
    res_val: List[Barcode] = []
    for dataset in val:
        res_val.extend(dataset)
    res_test: List[Barcode] = []
    for dataset in test:
        res_test.extend(dataset)
    return BarcodesDataset(res_train, res_val, res_test)


def filter_1d_qr(barcode):
    return barcode.marked_up_type not in [
        BarcodeType.DATA_MATRIX, BarcodeType.AZTEC, BarcodeType.PDF_417
    ]


def filter_ean_upc_a_qr(barcode):
    return filter_1d_qr(barcode) and barcode.marked_up_type not in [
        BarcodeType.ITF, BarcodeType.UPC_E, BarcodeType.CODE_39, BarcodeType.CODE_128
    ]


def parse_all_datasets():
    basic_dataset_path = BarcodeStorage.get_filepath_by_dataset_name("basic")
    saved_barcodes, is_ok = BarcodeStorage.load(basic_dataset_path)
    if not is_ok:
        yolo_train, yolo_val, yolo_test = parse_yolo_barcode_dataset(YOLO_BARCODE_DATASET_DIR)
        baber_train, barber_val, barber_test = parse_barber_dataset(BARBER_DATASET_DIR)
        sbd_train, sbd_val, sbd_test = parse_sbd(SBD_DIR)
        se_dmtx_syn_train, se_dmtx_syn_val, se_dmtx_syn_test = parse_se_dmtx_syn(SE_DMTX_SYN_DIR)
        barcodes = merge_datasets(
            [yolo_train, baber_train, sbd_train, se_dmtx_syn_train],
            [yolo_val, barber_val, sbd_val, se_dmtx_syn_val],
            [yolo_test, barber_test, sbd_test, se_dmtx_syn_test]
        )
        BarcodeStorage.save(barcodes, basic_dataset_path)
    else:
        barcodes = saved_barcodes
    return barcodes, barcodes.filter(filter_1d_qr), barcodes.filter(filter_ean_upc_a_qr)
