# -*- mode: python ; coding: utf-8 -*-
"""
Crossplatform Build Spec file for pyinstaller to install Gooey applications

command: `pyinstaller --windowed -F build-crossplatform.spec`

Also works for external binaries (Gooey as a Universal Frontend
cf. https://chriskiehl.com/article/gooey-as-a-universal-frontend)

Remove the external binary parts for a standard Gooey application
"""

import os
import sys

from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree

import gooey

gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, "languages"), prefix="gooey/languages")
gooey_images = Tree(os.path.join(gooey_root, "images"), prefix="gooey/images")


# Using Gooey as a Universal Frontend
# External binary name (assumption: placed in ./bin folder relative to the spec file)
external_binary = "EXTERNAL_BINARY_NAME"
if sys.platform.startswith("win"):
    external_binary += ".exe"

block_cipher = None

a = Analysis(
    ["gui.py"],
    binaries=[("./bin/" + external_binary, "./bin")],  # adds the external binary
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

options = [("u", None, "OPTION")]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    options,
    gooey_languages,  # Add them in to collected files
    gooey_images,  # Same here.
    name="APPNAME",
    debug=False,
    strip=None,
    upx=True,
    console=False,
    icon=os.path.join(gooey_root, "images", "program_icon.ico"),
)

# MacOS (https://docs.python.org/3/library/sys.html#sys.platform)
if sys.platform.startswith("darwin"):
    from PyInstaller.building.osx import BUNDLE

    # info_plist = {'addition_prop': 'additional_value'}
    info_plist = {}
    app = BUNDLE(
        exe,
        name="APPNAME.app",
        bundle_identifier=None,
        info_plist=info_plist,
    )
