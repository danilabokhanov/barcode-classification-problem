from .abstract_solver import AbstractBarcodeSolver
from barcodes.barcodes import BarcodeType, Barcode

from typing_extensions import override
from pathlib import Path
import jpype
import jpype.imports
import numpy as np
import sys


class BoofCVSolver(AbstractBarcodeSolver):
    MARKUP2BOOFCV = {
        BarcodeType.QR_CODE: "QR_CODE",
        BarcodeType.AZTEC: "AZTEC"
    }

    BOOFCV2MARKUP = {v: k for k, v in MARKUP2BOOFCV.items()}

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
        self._gc_ticks += 1
        if force_cleanup or self._gc_ticks >= self.GC_TICKS_PER_CYCLE:
            print("JVM resources stat before gc call", file=sys.stderr)
            print(self.get_memory_info(), file=sys.stderr)
            self.System.gc()
            if force_cleanup:
                self.System.gc()
            print("JVM resources stat after gc call", file=sys.stderr)
            print(self.get_memory_info(), file=sys.stderr)
            self._gc_ticks = 0

    def __init__(
        self,
        margin_rate,
        batched_mode,
        gc_calls_enabled=True,
        classpath=(
            "~/boofcv_jars/boofcv-types-1.1.6.jar",
            "~/boofcv_jars/boofcv-core-1.1.6.jar",
            "~/boofcv_jars/boofcv-io-1.1.6.jar",
            "~/boofcv_jars/boofcv-ip-1.1.6.jar",
            "~/boofcv_jars/boofcv-recognition-1.1.6.jar",
            "~/boofcv_jars/boofcv-feature-1.1.6.jar",
            "~/boofcv_jars/boofcv-geo-1.1.6.jar",
            "~/boofcv_jars/ddogleg-0.23.4.jar",
            "~/boofcv_jars/georegression-0.27.1.jar",
            "~/boofcv_jars/ejml-core-0.43.1.jar",
            "~/boofcv_jars/ejml-ddense-0.43.1.jar",
            "~/boofcv_jars/ejml-simple-0.43.1.jar",
        )
    ):
        super().__init__("boot_cv", margin_rate, batched_mode)

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

        from boofcv.struct.image import GrayU8, GrayF32
        from boofcv.io.image import ConvertBufferedImage
        from java.awt.image import BufferedImage
        from java.lang import System, Runtime
        from boofcv.factory.fiducial import FactoryFiducial
    
        self.FactoryFiducial = FactoryFiducial
        self.GrayU8 = GrayU8
        self.GrayF32 = GrayF32
        self.ConvertBufferedImage = ConvertBufferedImage
        self.BufferedImage = BufferedImage
        self.System = System
        self.Runtime = Runtime

        self.JByteArray = jpype.JArray(jpype.JByte)

        self._qr_detector = self.FactoryFiducial.qrcode(None, self.GrayU8)
        self._aztec_detector = self.FactoryFiducial.aztec(None, self.GrayU8)

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

    def buffered_image_to_gray(self, buffered_image):
        gray = self.GrayU8()
        self.ConvertBufferedImage.convertFrom(buffered_image, gray)
        return gray

    def _try_qr_code(self, gray_image):
        self._qr_detector.process(gray_image)
        
        detections = self._qr_detector.getDetections()
        if detections.size() > 0:
            qr = detections.get(0)
            return str(qr.message), BarcodeType.QR_CODE
        return None, None

    def _try_aztec(self, gray_image):
        self._aztec_detector.process(gray_image)
        
        detections = self._aztec_detector.getDetections()
        if detections.size() > 0:
            aztec = detections.get(0)
            return str(aztec.message), BarcodeType.AZTEC
        return None, None

    @override
    def _solve_one(self, barcode: Barcode) -> Barcode:
        buffered_image = self.numpy_to_buffered_image(barcode.image_array)
        gray_image = self.buffered_image_to_gray(buffered_image)

        supported_types = [
            t for t in barcode.possible_types 
            if t in self.MARKUP2BOOFCV
        ]

        for barcode_type in supported_types:
            text = None
            detected_type = None

            try:
                if barcode_type == BarcodeType.QR_CODE:
                    text, detected_type = self._try_qr_code(gray_image)
                elif barcode_type == BarcodeType.AZTEC:
                    text, detected_type = self._try_aztec(gray_image)

                if text is not None:
                    barcode.stats.actual_text = text
                    barcode.stats.actual_type = detected_type
                    return barcode

            except Exception:
                pass

        barcode.stats.actual_text = None
        barcode.stats.actual_type = None
        return barcode
