pyinstaller --onefile --paths=. -n DrawingGame game\main.py

move dist\DrawingGame.exe game\

rmdir /s /q build
rmdir /s /q dist
