@echo off
set /p "folder=Directory with the folders to be used  (Emotes?)>>>"
set /p "cols=Columns per Page  (10?)>>>"
set /p "rows=Rows per Page  (6?)>>>"
GenerateMacroDeckProfile.py -c %cols% -r %rows% -d %folder%
echo "Finished"
echo ""
echo "Next step: Copy all Folders inside %folder% into the iconpacks directory. If a Folder already exists, copy only the emote files (skip the ExtensionManifest.json).
start %windir%\explorer.exe "%appdata%\Macro Deck\iconpacks\"
pause