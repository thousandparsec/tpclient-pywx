
cd dist
mkdir temp
cd temp
7z x ..\library.zip
del ..\library.zip

7z a -tzip -mx9 "..\library.zip" -r
cd ..
rd /S /Q temp