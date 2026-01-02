@echo off
echo ==========================================
echo      Building FolderCrafter (Dir Mode) 📂
echo ==========================================

REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist

REM Build command
REM --onedir: Create a folder containing the executable (faster startup)
REM --noconsole: Hide the terminal window
REM --icon: Set application icon
REM --add-data: Include CustomTkinter and the Icon file
pyinstaller --noconfirm --onedir --windowed --name "FolderCrafter" --icon "foldercrafter.ico" --add-data "C:\Users\amras\AppData\Local\Programs\Python\Python312\Lib\site-packages\customtkinter;customtkinter/" --add-data "foldercrafter.ico;." "main.py"

echo.
echo ==========================================
echo      Build Complete! 🎉
echo      Check 'dist\FolderCrafter\FolderCrafter.exe'
echo ==========================================
pause
