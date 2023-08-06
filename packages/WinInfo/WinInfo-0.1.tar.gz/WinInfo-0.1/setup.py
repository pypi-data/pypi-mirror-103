from setuptools import setup


'''
from WinInfo import (
    SystemInfo,
    HardwareInfo,
    NetworkInfo,
    AntiAnalysis
)

print(SystemInfo)
print(HardwareInfo)
print(NetworkInfo)
print(AntiAnalysis)

'''


setup (
    name="WinInfo",
    version=0.1,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Python module to get system information",
    packages=["WinInfo"],
    install_requires=["PyMI"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)

