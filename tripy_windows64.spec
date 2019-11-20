# -*- mode: python ; coding: utf-8 -*-


import PyInstaller.config
import os
PyInstaller.config.CONF['distpath'] = "./engine/"
block_cipher = None

_bin_dirpath = 'bin/win64'
python_engine = [(branch[1], os.path.dirname(os.path.join(_bin_dirpath, branch[0]))) for branch in Tree(_bin_dirpath)]
added_files = [
    ('cache/.include', 'cache/'),
    ('temp/.include', 'temp/'),
    ('config/config.json', 'config/')
]
added_files.extend(python_engine)
print(python_engine)
# added_files.extend(python_engine)
a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='windows')
