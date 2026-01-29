from PyInstaller.utils.hooks import copy_metadata
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['cslckrwbcl.py'],
    pathex=[],
    binaries=[],
    datas=[
        *copy_metadata('imageio'),
        *copy_metadata('imageio_ffmpeg'),
    ],
    hiddenimports=[
        'bsod',
        'imageio',
        'imageio_ffmpeg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='cslckrwbcl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',
        'python312.dll',  # Use your specific python version (e.g., 311, 312, 313)
        'imageio_ffmpeg-win64.exe', # The actual FFmpeg binary
        'libopenblas.dll' # Common in image/math libs that triggers GUARD_CF
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['favicon.ico'],
    onefile=True,
)
