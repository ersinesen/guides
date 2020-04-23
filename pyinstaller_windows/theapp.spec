# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew, angle

block_cipher = None

# to build package in azure vm (no opengl >2.0 so use opengl es)
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


a = Analysis(['main.py'],
             pathex=['FULL_PATH_TO_THEAPP'],
             binaries=[],
             datas=[],
             #hiddenimports=['win32timezone'] + kivy_deps_all['hiddenimports'] + kivy_factory_modules,
             hiddenimports=['win32timezone'] ,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Theapp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          icon='icon.ico')

coll = COLLECT(exe, Tree('THEPATH\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
               strip=False,
               upx=False,
               name='Theapp')