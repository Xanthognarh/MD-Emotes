@echo off
set /p "Kanal=Twitch Name >>>"
fetch_from_api.py -c %Kanal% -d Emotes
echo "Finished"
pause