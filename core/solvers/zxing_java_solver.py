from .abstract_solver import AbstractBarcodeSolver
from barcodes.barcodes import BarcodeType, Barcode

from typing_extensions import override
from pathlib import Path
import jpype
import jpype.imports
import numpy as np
import sys

class ZXingJavaSolver(AbstractBarcodeSolver):
    MARKUP2ZXING_JAVA = {
        BarcodeType.QR_CODE: "QR_CODE",
        BarcodeType.DATA_MATRIX: "DATA_MATRIX",
        BarcodeType.EAN_13: "EAN_13",
        BarcodeType.UPC_A: "UPC_A",
        BarcodeType.UPC_E: "UPC_E",
        BarcodeType.CODE_128: "CODE_128",
        BarcodeType.CODE_39: "CODE_39",
        BarcodeType.EAN_8: "EAN_8",
        BarcodeType.ITF: "ITF",
        BarcodeType.PDF_417: "PDF_417",
        BarcodeType.AZTEC: "AZTEC",
    }

    ZXING_JAVA2MARKUP = {v: k for k, v in MARKUP2ZXING_JAVA.items()}

    GC_TICKS_PER_CYCLE = 100

    def get_memory_info(self):
        runtime = self.Runtime.getRuntime()
        total = runtime.totalMemory()
        free = runtime.freeMemory()
        used = total - free
        max_mem = runtime.maxMemory()
        
        return {
            'used_mb': used / (1024 * 1024),
            'free_mb': free / (1024 * 1024),
            'total_mb': total / (1024 * 1024),
            'max_mb': max_mem / (1024 * 1024),
        }

    @override
    def consider_running_cleanup(self, force_cleanup=False) -> None:
        if not force_cleanup and not self._gc_calls_enabled:
            return
        mem_info = self.get_memory_info()
        if force_cleanup or mem_info['used_mb'] > 500:
            print("JVM resources stat before gc call", file=sys.stderr)
            print(mem_info, file=sys.stderr)
            self.System.gc()
            if force_cleanup:
                self.System.gc()
            mem_info = self.get_memory_info()
            print("JVM resources stat after gc call", file=sys.stderr)
            print(mem_info, file=sys.stderr)

    def __init__(
        self,
        margin_rate,
        batched_mode,
        gc_calls_enabled=True,
        classpath=(
            "~/zxing_jars/core-3.5.1.jar",
            "~/zxing_jars/javase-3.5.1.jar",
        ),
    ):
        super().__init__("ZxingJava", margin_rate, batched_mode)

        if not jpype.isJVMStarted():
            classpath = [str(Path(p).expanduser()) for p in classpath]
            
            jvm_args = [
                '-Xms2g',
                '-Xmx4g',
                '-XX:+UseG1GC',
                '-XX:MaxGCPauseMillis=1000',
                '-XX:GCTimeRatio=99',
            ]

            jpype.startJVM(*jvm_args, classpath=classpath)

        from com.google.zxing import (
            MultiFormatReader,
            BarcodeFormat,
            DecodeHintType,
            BinaryBitmap,
        )
        from com.google.zxing.common import HybridBinarizer
        from com.google.zxing.client.j2se import BufferedImageLuminanceSource
        from java.awt.image import BufferedImage
        from java.util import EnumSet, HashMap
        from java.lang import System, Runtime

        self.MultiFormatReader = MultiFormatReader
        self.BarcodeFormat = BarcodeFormat
        self.DecodeHintType = DecodeHintType
        self.BinaryBitmap = BinaryBitmap
        self.HybridBinarizer = HybridBinarizer
        self.BufferedImageLuminanceSource = BufferedImageLuminanceSource
        self.BufferedImage = BufferedImage
        self.EnumSet = EnumSet
        self.HashMap = HashMap
        self.System = System
        self.Runtime = Runtime

        self.JByteArray = jpype.JArray(jpype.JByte)

        self._reader = self.MultiFormatReader()

        self._gc_calls_enabled = gc_calls_enabled
        self._gc_ticks = 0
        self.consider_running_cleanup(force_cleanup=True)

    def numpy_to_buffered_image(self, arr: np.ndarray):
        h, w = arr.shape[:2]

        if arr.ndim == 2:
            img = self.BufferedImage(w, h, self.BufferedImage.TYPE_BYTE_GRAY)
        else:
            img = self.BufferedImage(w, h, self.BufferedImage.TYPE_3BYTE_BGR)
        
        raster = img.getRaster()

        if arr.ndim == 2:
            data = arr.tobytes()
        else:
            data = arr[:, :, ::-1].tobytes()

        buf = self.JByteArray(data)
        raster.setDataElements(0, 0, w, h, buf)

        return img

    def create_formats_from_hints(self, hints):
        formats = self.EnumSet.noneOf(self.BarcodeFormat)
        for hint in hints:
            fmt = self.MARKUP2ZXING_JAVA[hint]
            formats.add(getattr(self.BarcodeFormat, fmt))
        return formats

    @override
    def _solve_one(self, barcode: Barcode) -> Barcode:
        buffered_image = self.numpy_to_buffered_image(barcode.image_array)
        source = self.BufferedImageLuminanceSource(buffered_image)
        bitmap = self.BinaryBitmap(self.HybridBinarizer(source))

        hints = self.HashMap()
        formats = self.create_formats_from_hints(barcode.possible_types)
        if not formats.isEmpty():
            hints.put(self.DecodeHintType.POSSIBLE_FORMATS, formats)
        hints.put(self.DecodeHintType.TRY_HARDER, True)
        self._reader.setHints(hints)

        try:
            result = self._reader.decodeWithState(bitmap)
            barcode.stats.actual_text = str(result.getText())
            barcode.stats.actual_type = self.ZXING_JAVA2MARKUP.get(
                result.getBarcodeFormat().name()
            )
        except Exception:
            barcode.stats.actual_text = None
            barcode.stats.actual_type = None
        finally:
            self._reader.reset()
        return barcode
