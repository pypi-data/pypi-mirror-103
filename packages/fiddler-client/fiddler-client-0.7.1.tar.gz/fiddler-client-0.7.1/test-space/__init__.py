"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""
from ..fiddler import utils
from ..fiddler._version import __version__
from ..fiddler.client import Fiddler, PredictionEventBundle
from ..fiddler.core_objects import (
    BatchPublishType,
    Column,
    DatasetInfo,
    DataType,
    ExplanationMethod,
    MLFlowParams,
    ModelDeploymentParams,
    ModelInfo,
    ModelInputType,
    ModelTask,
)
from ..fiddler.fiddler_api import FiddlerApi
from ..fiddler.utils import ColorLogger
from ..fiddler.validator import PackageValidator, ValidationChainSettings, ValidationModule

__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerApi',
    'MLFlowParams',
    'ModelDeploymentParams',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'ExplanationMethod',
    'PredictionEventBundle',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
]
