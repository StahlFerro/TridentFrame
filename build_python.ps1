Remove-item .\release\tridentframe_win -Recurse -Force
pyinstaller tridentframe_win.spec
