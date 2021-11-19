.\venv\Scripts\activate.bat
pyinstaller main.spec --onefile --windowed
copy .\TMLSaveEditor\Sprite .\dist\main\Sprite