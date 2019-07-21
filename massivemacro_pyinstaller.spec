block_cipher = None

a = Analysis(
	["run.py"],
	pathex=["."],
	binaries=[],
	datas=[],
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False
)

pyz = PYZ(
	a.pure,
	a.zipped_data,
	cipher=block_cipher
)

exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	[],
	name="massivemacro",
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	upx_exclude=[],
	runtime_tmpdir=None,
	console=False,
	icon="windows\\icon.ico"
)

app = BUNDLE(
	exe,
	name="MassiveMacro.app",
	icon="macos/icon.icns",
	bundle_identifier="com.therandomlabs.massivemacro",
	info_plist={
		"CFBundleName": "MassiveMacro"
	}
)
