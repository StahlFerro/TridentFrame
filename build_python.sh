rm -rvf build/
rm -rvf release/tripy_linux/
pyinstaller tripy_linux.spec
# rm dist/main
rm release/tripy_linux.tar.gz
tar -czvf release/tripy_linux.tar.gz release/tripy_linux/
