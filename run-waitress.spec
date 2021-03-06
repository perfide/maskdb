#!/usr/bin/env pyinstaller
# -*- coding: utf-8 -*-

"""Configuration for pyinstaller"""


import os

block_cipher = None

BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, 'maskdb')

a = Analysis(  # noqa: F821
    ['run-waitress.py'],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        (os.path.join(APP_DIR, 'templates'), 'templates'),
        (os.path.join(APP_DIR, 'translations'), 'translations'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # noqa: F821
exe = EXE(  # noqa: F821
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='maskdb-waitress',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='maskdb-waitress',
)
