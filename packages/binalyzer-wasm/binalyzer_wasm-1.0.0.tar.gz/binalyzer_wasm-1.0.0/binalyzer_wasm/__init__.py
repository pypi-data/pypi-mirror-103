# -*- coding: utf-8 -*-
"""
    binalyzer_wasm
    ~~~~~~~~~~~~~~

    Binalyzer WebAssembly Extension

    :copyright: 2020 Denis Vasilík
    :license: MIT, see LICENSE for details.
"""

name = "binalyzer_wasm"

__tag__ = "v1.0.0"
__build__ = 15
__version__ = "{}".format(__tag__)
__commit__ = "87ead22"

from .extension import WebAssemblyExtension
from .wasm import (
    LEB128UnsignedBindingValueProvider,
    LEB128SizeBindingValueProvider,
)
