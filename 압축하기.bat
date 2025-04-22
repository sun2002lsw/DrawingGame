pyinstaller --onefile --paths=. -n DrawingGame game\main.py
powershell -command "Compress-Archive -Path dist\DrawingGame.exe, game\data -DestinationPath DrawingGame.zip"

rmdir /s /q build
rmdir /s /q dist
del DrawingGame.spec
del main.spec
