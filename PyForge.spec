# PyInstaller build recipe. Used by the release workflow and by
#   pyinstaller PyForge.spec
#
# One-DIR, not one-file: the app relaunches its own executable as the
# interpreter every time you run code or tests, and a one-file build would
# re-extract the whole archive on every single run.
import sys

block_cipher = None

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Nothing here is used by the app; dropping them keeps the build small.
    excludes=[
        "numpy", "pandas", "matplotlib", "scipy", "PIL", "pytest",
        "setuptools", "pip", "wheel", "test", "unittest",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PyForge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    # No console window. The child interpreter rebinds its own stdio, see
    # runner.run_child().
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="PyForge",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="PyForge.app",
        icon=None,
        bundle_identifier="dev.senseiissei.pyforge",
        info_plist={
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "11.0",
        },
    )
