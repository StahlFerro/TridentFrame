from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = {
    'packages': [], 'excludes': [],
    'include_files': [
        ('cache/.include', 'cache/.include'),
        ('previews/.include', 'previews/.include'),
        ('temp/.include', 'temp/.include'),
        ('config/imagers.json', 'config/imagers.json'),
        ('config/settings.json', 'config/settings.json'),
    ],
    'build_exe': 'engine/windows_cx/'
}

base = 'Console'

executables = [
    Executable('main.py', base=base, target_name='tridentengine.exe')
]

setup(name='TridentFrame',
      version='0.1.0',
      description='Animated image manipulation program',
      options={'build_exe': build_exe_options},
      executables=executables)
