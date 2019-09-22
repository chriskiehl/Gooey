# -*- mode: python ; coding: utf-8 -*-

import gooey
gooey_root = os.path.dirname(gooey.__file__)

block_cipher = None

a = Analysis(['APPNAME.py'],  # replace me with your path
             pathex=['/path/to/APP.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))
