REM compile and generate EXE file. See https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish for more informations
dotnet publish -p:PublishSingleFile=True -r win-x64 --self-contained false -c Release -o .