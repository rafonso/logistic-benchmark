REM clean directory
dotnet clean -o .
rmdir /q /s bin
rmdir /q /s obj
del /q *.pdb
del /q *.exe