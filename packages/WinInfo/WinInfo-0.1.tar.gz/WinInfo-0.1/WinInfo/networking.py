#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["NetworkInfo"]

# Import modules
from wmi import WMI
from struct import unpack
from ipaddress import IPv4Address
from urllib.request import urlopen
from socket import socket, AF_INET, SOCK_DGRAM
from ctypes import windll, c_buffer, c_ulong, sizeof, byref


class NetworkInfo(object):
	
	def __init__(self):
		self.wmi = WMI()

	def __str__(self) -> str:
		return f"""
		LocalIP="{self.LocalIP}"
		PublicIP="{self.PublicIP}"
		BSSID="{self.RouterMac}"
		DefaultGateway="{self.DefaultGateway}"
		""".replace("		", "")

	@property
	def LocalIP(self) -> str:
		with socket(AF_INET, SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))
			return s.getsockname()[0]

	@property
	def PublicIP(self) -> str:
		try:
			response = urlopen("http://ip-api.com/line?fields=query")
		except Exception:
			return "127.0.0.1"
		else:
			if response.status == 200:
				return response.read().decode().strip('\n')

	@property
	def DefaultGateway(self) -> str:
		query = "SELECT NextHop FROM Win32_IP4RouteTable WHERE Destination='0.0.0.0' AND Mask='0.0.0.0'"
		results = self.wmi.query(query)
		if len(results) > 0:
			return results[0].NextHop
		return "127.0.0.1"

	@property
	def RouterMac(self) -> str:
		return self.GetMacAddress(self.DefaultGateway)

	@staticmethod
	def GetMacAddress(host):
		inetaddr = int(IPv4Address(".".join(host.split(".")[::-1])))
		buffer = c_buffer(6)
		addlen = c_ulong(sizeof(buffer))
		if windll.Iphlpapi.SendARP(inetaddr, 0, byref(buffer), byref(addlen)) == 0:
			macaddr = ""
			for intval in unpack("BBBBBB", buffer):
				repl = "0x" if intval > 15 else "x"
				macaddr = ":".join([macaddr, hex(intval).replace(repl, "")])
			return macaddr.upper()[1:]
		return "Unknown"
