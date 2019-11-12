rm -rvf dist/tridentframe_py
pyinstaller tridentframe.spec
rm dist/main
rm tridentframe_py.tar.gz
tar -czvf dist/tridentframe_py.tar.gz dist/tridentframe_py/
