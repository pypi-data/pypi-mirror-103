#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["SystemInfo"]

# Import modules
from wmi import WMI
from platform import node
from ctypes import windll
from getpass import getuser
from locale import windows_locale
from winreg import (
	ConnectRegistry,
	OpenKey,
	QueryValueEx,
	HKEY_LOCAL_MACHINE
)


class SystemInfo(object):

	def __init__(self):
		self.wmi = WMI()

	def __str__(self) -> str:
		return f"""
		CompName="{self.CompName}"
		UserName="{self.UserName}"
		IsAdmin={self.IsAdmin}
		OSName="{self.OSName}"
		UILang="{self.UILang}"
		""".replace("		", "")

	# Get machine name, user name, is admin
	CompName = node()
	UserName = getuser()
	IsAdmin = windll.shell32.IsUserAnAdmin() != 0

	# Get Windows version name
	# Example output: "Windows 10 Pro"
	@property
	def _WindowsVersion(self) -> str:
		name = self.wmi.Win32_OperatingSystem()[0].Name
		return ' '.join(name.split('|')[0].split(' ')[1:])

	# Get Bit version
	# Example output: 32 or 64
	@property
	def _BitVersion(self) -> int:
		path = "HARDWARE\\Description\\System\\CentralProcessor\\0"
		a_reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
		a_key = OpenKey(a_reg, path)
		a_val = QueryValueEx(a_key, "Identifier")
		return 32 if "x86" in a_val else 64

	# Get operating system name 
	# Example output: "Windows 10 Pro (64 bit)"
	@property
	def OSName(self) -> str:
		bit = self._BitVersion
		name = self._WindowsVersion
		return f"{name} ({bit} bit)"

	# Get user interface language
	# Example output: "RU"
	@property
	def UILang(self) -> str:
		code = windll.kernel32.GetUserDefaultUILanguage()
		return windows_locale[code].split('_')[-1]
