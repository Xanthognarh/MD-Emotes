# MD-Emotes
Use your Macro Deck 2 to write Twitch/7TV Emotes. This tool downloads the Emotes and creates a new Profile in Macro Deck 2 with the Emotes as Buttons.

## Installation
Python already installed? Simply copy the `*.py` and `*.bat` files into the same directory.

No Python installed? Download the released `*.exe` files.

## Usage
Tip: Test with one channel and a few emotes, but for the final product, it is recommended to do the work with all channels and emotes at once.
1. Run `1_CLI-Download-Emotes.bat`, then enter the Twitch channel name. Repeat this step for all the channels you want.
2. Launch Macro Deck 2 and read the number of columns and rows. If you haven't used Macro Deck before, set these values as you like. The first button will be used for returning to the previous page. So you can use (cols*rows - 1) emotes per page (called 'folder' in Macro Deck). 
3. Launch your File Explorer and create a new folder that represents your new Macro Deck profile. You can also use the `Emotes` folder.
4. Within this directory, each folder represents one page in Macro Deck. The folder name is used for the Macro Deck page name. Arrange the emotes in the folders and check for the maximum amount (step 2). 
5. Make sure, that the directory contains only the files/folders you want to include.
6. Exit Macro Deck 2
7. Run `2_CLI-Insert-Emotes-MD.bat` and enter the directory name (containing the page folders), the number of cols, and the number of rows per page.
8. Copy all Folders containing the emotes into the `iconpacks` directory. This directory should have been opened by Step 7. Do not rename the folders or files! If a folder already exists, copy only the emote files (do not copy the `ExtensionManifest.json`).
9. Done
10. Launch Macro Deck 2. Select the new profile from the drop-down menu in the middle of the top of the window. You can rename it using the pencil icon beside it.
11. Change the profile for other devices: Switch to the 'device' tab on the left side of the window. Here you can change the profile for each device.
12. Create buttons to switch between profiles: Create a new button and select Device → Change Profile as  the action.

## Credits
This tool uses a modified version of [Lee-7723/twitch-emotes-downloader](https://github.com/Lee-7723/twitch-emotes-downloader) `fetch_from_api.py`