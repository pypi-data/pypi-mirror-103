#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["HardwareInfo"]

# Import modules
from wmi import WMI
from ctypes import windll


class HardwareInfo(object):

	def __init__(self):
		self.wmi = WMI()

	def __str__(self) -> str:
		return f"""
		CPUName="{self.CPUName}"
		GPUName="{self.GPUName}"
		RAMAmount={self.RAMAmount}
		Model="{self.Model}"
		Manufacturer="{self.Manufacturer}"
		ScreenResolution={self.ScreenResolution}
		""".replace("		", "")

	@property
	def CPUName(self) -> str:
		return self.wmi.Win32_Processor()[0].Name

	@property
	def GPUName(self) -> str:
		return self.wmi.Win32_VideoController()[0].Name

	@property
	def RAMAmount(self) -> int:
		count = self.wmi.Win32_ComputerSystem()[0].TotalPhysicalMemory
		return int(float(count) / (1024 * 1024))

	@property
	def Model(self) -> str:
		return self.wmi.Win32_ComputerSystem()[0].Model

	@property
	def Manufacturer(self) -> str:
		return self.wmi.Win32_ComputerSystem()[0].Manufacturer

	@property
	def ScreenResolution(self) -> tuple:
		x = windll.user32.GetSystemMetrics(0)
		y = windll.user32.GetSystemMetrics(1)
		return x, y
