# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
added_files = [
    ( './Icon', 'Icon' ),
]

a = Analysis(['/Users/IsaacYang/MatchBox-Converter/MatchBoxConverter.py'],
             pathex=['/Users/IsaacYang/MatchBox-Converter'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='MatchBoxConverter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=True,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='/Users/IsaacYang/MatchBox-Converter/Icon/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NewUI')
app = BUNDLE(coll,
             name='MatchBox+ MasterPlan Converter UI.app',
             icon='/Users/IsaacYang/MatchBox-Converter/Icon/Icon.icns',
             bundle_identifier='com.Luxshare-ict.HSSW IsaacYang.ConverterUI',
             info_plist={
              'NSPrincipalClass': 'NSApplication',
              'NSAppleScriptEnabled': False,
              'CFBundleDisplayName': 'MatchBox+ MasterPlan Converter UI',
              'CFBundleIdentifier': 'com.Luxshare-ict.HSSW IsaacYang.ConverterUI',
              'CFBundleGetInfoString': 'Convert MasterPlan to MatchBox CSV',
              'CFBundleVersion': '1.0.3_Beta',
              'CFBundleShortVersionString': '1.0.3_Beta',
              'NSHumanReadableCopyright': 'Copyright © 2021, Luxshare-ICT HSSW Isaac Yang, All Rights Reserved',
             },
            )
