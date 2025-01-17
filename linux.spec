# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None


a = Analysis(
    ['src/pygpt_net/app.py'],
    pathex=[
        'src',
        'src/pygpt_net'
    ],
    binaries=[],
    datas=collect_data_files('opentelemetry.sdk', 'pinecode') + [  # chromadb, pinecode hack
        ('src/pygpt_net/data/config/presets/*', 'data/config/presets'),
        ('src/pygpt_net/data/config/config.json', 'data/config'),
        ('src/pygpt_net/data/config/models.json', 'data/config'),
        ('src/pygpt_net/data/config/modes.json', 'data/config'),
        ('src/pygpt_net/data/config/settings.json', 'data/config'),
        ('src/pygpt_net/data/config/settings_section.json', 'data/config'),
        ('src/pygpt_net/data/locale/*', 'data/locale'),
        ('src/pygpt_net/data/css/*', 'data/css'),
        ('src/pygpt_net/data/fonts/Lato/*', 'data/fonts/Lato'),
        ('src/pygpt_net/data/logo.png', 'data'),
        ('src/pygpt_net/data/icon.ico', 'data'),
        ('src/pygpt_net/data/icon_tray_idle.ico', 'data'),
        ('src/pygpt_net/data/icon_tray_busy.ico', 'data'),
        ('src/pygpt_net/data/icon_tray_error.ico', 'data'),
        ('src/pygpt_net/CHANGELOG.txt', '.'),
        ('README.md', '.'),
        ('src/pygpt_net/__init__.py', '.'),
        ('venv/lib/python3.10/site-packages/llama_index/VERSION', 'llama_index/'),  # llama-index hack
        ('venv/lib/python3.10/site-packages/langchain/chains', 'langchain/chains'),  # llama-index hack
        ('venv/lib/python3.10/site-packages/opentelemetry_sdk-1.22.0.dist-info/*', 'opentelemetry_sdk-1.22.0.dist-info'), # chromadb hack
        ('venv/lib/python3.10/site-packages/pinecone/__version__', 'pinecone'),  # pinecode hack
    ],
    hiddenimports=[
    'pinecode',
    'opentelemetry',
    'opentelemetry.sdk',
    'onnxruntime',
    'tokenizers',
    'tiktoken_ext', 
    'tiktoken_ext.openai_public', 
    'wikipedia', 
    'pydub'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='pygpt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/pygpt_net/data/icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Linux',
)
