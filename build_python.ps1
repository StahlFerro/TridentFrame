Remove-Item .\build\ -Recurse -Force
Remove-Item .\dist\main -Recurse -Force
Remove-Item .\dist\tridentframe_py -Recurse -Force
pyinstaller tridentframe_win.spec
