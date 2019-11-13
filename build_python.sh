rm -rvf build/
rm -rvf dist/tridentframe_py
pyinstaller tridentframe_linux.spec
# rm dist/main
rm tridentframe_linux.tar.gz
tar -czvf dist/tridentframe_linux.tar.gz dist/tridentframe_linux/
