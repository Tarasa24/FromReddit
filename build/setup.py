import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [], "excludes": [],  "build_exe": "out"}

target = Executable(
    script="../FromReddit.py",
    base=None,
    icon="sword.ico")

setup(name = "FromReddit",
      version = "0.1",
      description = "AskReddit questions on demand",
      options = {"build_exe": build_exe_options},
      executables = [target])