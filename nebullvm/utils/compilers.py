from typing import List
import cpuinfo
import torch

from nebullvm.base import ModelCompiler

from hyperparameter import auto_param


def tvm_is_available() -> bool:
    try:
        import tvm  # noqa F401

        return True
    except ImportError:
        return False


def bladedisc_is_available() -> bool:
    try:
        import torch_blade  # noqa F401

        return True
    except ImportError:
        return False


def torch_tensorrt_is_available() -> bool:
    try:
        import torch_tensorrt  # noqa F401

        return True
    except ImportError:
        return False


def deepsparse_is_available() -> bool:
    try:
        import deepsarse  # noqa F401
    except ImportError:
        return False
    else:
        return True


@auto_param("nebullvm.compilers")
def selector(enabled: List[str] = None):
    return enabled


def select_compilers_from_hardware_onnx():
    if selector() is not None:
        return [x for x in ModelCompiler if x.value in selector()]
    compilers = [ModelCompiler.ONNX_RUNTIME]
    if tvm_is_available():
        compilers.append(ModelCompiler.APACHE_TVM)
    if torch.cuda.is_available():
        compilers.append(ModelCompiler.TENSOR_RT)
    cpu_raw_info = cpuinfo.get_cpu_info()["brand_raw"].lower()
    if "intel" in cpu_raw_info:
        compilers.append(ModelCompiler.OPENVINO)
    return compilers
