# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py', 'model.py', 'history.py', 'source.py', 'ware.py', 'js.py', 'network.py'],
             pathex=['.'],
             binaries=None,
             datas=[('html/*.html', 'html'), ('js/*.js', 'js')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='daily-specials',
          debug=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='daily-specials')
