# -*- coding: utf-8 -*-
"""
    binalyzer_cli
    ~~~~~~~~~~~~~

    A library supporting the analysis of binary data.

    :copyright: 2021 Denis Vasilík
    :license: MIT, see LICENSE for details.
"""

name = "binalyzer_cli"

__tag__ = "v1.0.0"
__build__ = 47
__version__ = "{}".format(__tag__)
__commit__ = "343301"

from .cli import (
    TemplateAutoCompletion,
    ExpandedFile,
    BasedIntParamType,
)