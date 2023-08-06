#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["SystemInfo", "NetworkInfo", "HardwareInfo", "AntiAnalysis"]

# Import modules
from sys import version_info, platform

# Import packages
from .system import SystemInfo as __SystemInfoClass
from .hardware import HardwareInfo as __HardwareInfoClass
from .networking import NetworkInfo as __NetworkInfoClass
from .antianalysis import AntiAnalysis as __AntiAnalysisClass

# Check operating system
assert 3 <= version_info.major, "Python >3.8 required to run script!"
assert platform[:3] == "win", "Script created only for Windows systems!"

# Init classes
SystemInfo = __SystemInfoClass()
NetworkInfo = __NetworkInfoClass()
HardwareInfo = __HardwareInfoClass()
AntiAnalysis = __AntiAnalysisClass()
