@echo off
echo ==========================================
echo      Building FolderCrafter... 🚀
echo ==========================================

pyinstaller --noconfirm --onefile --windowed --name "FolderCrafter" --add-data "C:\Users\amras\AppData\Local\Programs\Python\Python312\Lib\site-packages\customtkinter;customtkinter/" "main.py"

echo.
echo ==========================================
echo      Build Complete! 🎉
echo      Check the 'dist' folder for FolderCrafter.exe
echo ==========================================
pause
