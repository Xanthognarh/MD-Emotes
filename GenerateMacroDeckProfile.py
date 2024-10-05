#Set the size of one page. The first field will be reserved for a "back"-Button
cols=10
rows=6

#Set the Foldername/Path where all the folders are. 
folderpath="Emotes"
#The name of the folders is used as foldername in macro deck.
#In each folder must be a maximum of (cols*rows - 1) emote files.

#Set the name of the profile for macro deck.
profilename="Twitch-Emotes"

#Don't edit below

import os,sys, json, time
import sqlite3
folderlist=next(os.walk(folderpath))[1]
output=""
children=[]
print("Import Folders:",folderlist)
for folder in folderlist:
    files=os.listdir(os.path.join(folderpath,folder))
    try:
        files.remove("ExtensionManifest.json")
    except:
        pass
    children.append('"42'+folder+'"')
    
    output+='{"BUFFER_SIZE": 1048576,"IsRootFolder": false,"FolderId": "42'+folder+'","DisplayName": "'+folder+'","Childs": [],"ActionButtons": ['
    output+='{"Guid": "'+folder+'-backToRoot","State": false,"IconOff": "Macro Deck colorful generic icons.1630428270904","IconOn": "","BackColorOff": "35, 35, 35","BackColorOn": "35, 35, 35","LabelOff": {"LabelText": "*Home*","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},"LabelOn": {"LabelText": "","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},"Position_X": 0,"Position_Y": 0,"StateBindingVariable": "","Actions": [{"$type": "SuchByte.MacroDeck.Folders.Plugin.GoToParentFolder, Macro Deck 2","Name": "Gehe zu übergeordnetem Ordner","Description": "Ändert den Ordner auf dem Gerät, das die Aktion ausgeführt hat, zu dem übergeordnetem Ordner","CanConfigure": false}],"ActionsRelease": [],"ActionsLongPress": [],"ActionsLongPressRelease": [],"EventListeners": [],"ModifierKeyCodes": 0,"KeyCode": 0},'
    for index, file in enumerate(files):
        if index+1>cols*rows:
            print("No more free fields left. Only the first "+str(cols*rows-1)+" emotes have been inserted.")
            break

        fname=file.split(".")[0]
        Guid="Generated-"+folder+"-"+str(index)
        Iconset=folder
        output+='{"Guid": "'+Guid+'","State": false,"IconOff": "'+Iconset+'.'+fname+'","IconOn": "","BackColorOff": "35, 35, 35","BackColorOn": "35, 35, 35","LabelOff": {"LabelText": "'+fname+'","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},"LabelOn": {"LabelText": "","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},'

        y=(index+1)//10
        x=(index+1)%10
        output+=r'"Position_X": '+str(x)+',"Position_Y": '+str(y)+r',"StateBindingVariable": "","Actions": [{"$type": "SuchByte.WindowsUtils.Actions.WriteTextAction, Windows Utils","Name": "Text schreiben","Description": "Schreibt einen konfigurierten Text in das markierte Textfeld","CanConfigure": true,"Configuration": "{\r\n  \"text\": \"'+fname+r' \"\r\n}","ConfigurationSummary": "'+fname+' "}],"ActionsRelease": [],"ActionsLongPress": [],"ActionsLongPressRelease": [],"EventListeners": [],"ModifierKeyCodes": 0,"KeyCode": 0},'
    output=output[:-1]
    output+='],"ApplicationsFocusDevices": [],"ApplicationToTrigger": ""},'
output=output[:-1]



ProfileId=str(round(time.time()))+"Emotes"
profileoutput='{"BufferSize":1048576,"ProfileId": "'+ProfileId+'","DisplayName": "'+profilename+'","Folders": ['
profileoutput+='{"BUFFER_SIZE": 1048576,"IsRootFolder": true,"FolderId": "42","DisplayName": "Emotes","Childs": ['+",".join(children)+'],"ActionButtons": ['
for index,folder in enumerate(folderlist):
    ExtensionManifest='{"type": 1,"name": "'+folder+'","author": "","repository": "","packageId": "'+folder+'","version": "1.0.0","target-plugin-api-version": 40,"dll": ""}'
    with open(os.path.join(folderpath,folder,"ExtensionManifest.json"),"w") as f:
        f.write(ExtensionManifest)
    Guid="GeneratedLink-"+folder+"-"+str(index)
    y=(index+1)//10
    x=(index+1)%10
    profileoutput+='{"Guid": "'+Guid+'","State": false,"IconOff": "","IconOn": "","BackColorOff": "35, 35, 35","BackColorOn": "35, 35, 35","LabelOff": {"LabelText": "'+folder+'","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},"LabelOn": {"LabelText": "","LabelPosition": 2,"LabelColor": "White","Size": 6.0,"FontFamily": "Impact","LabelBase64": ""},"Position_X": '+str(x)+',"Position_Y": '+str(y)+',"StateBindingVariable": "","Actions": [{"$type": "SuchByte.MacroDeck.Folders.Plugin.FolderSwitcher, Macro Deck 2","Name": "Ordner ändern","CanConfigure": true,"Description": "Ändert den Ordner auf dem Gerät, das die Aktion ausgeführt hat, zu dem eingestellten Ordner","Configuration": "42'+folder+'","ConfigurationSummary": "'+folder+'"}],"ActionsRelease": [],"ActionsLongPress": [],"ActionsLongPressRelease": [],"EventListeners": [],"ModifierKeyCodes": 0,"KeyCode": 0},'
profileoutput=profileoutput[:-1]
profileoutput+='],"ApplicationsFocusDevices": [],"ApplicationToTrigger": ""},'
profileoutput+=output
profileoutput+='],"Rows": '+str(rows)+',"Columns": '+str(cols)+',"ButtonSpacing": 4,"ButtonRadius": 40,"ButtonBackground": true,"ProfileTarget": 0,"ButtonsCustomizable": true}'



#Open SQLite Database:
dbpath=os.getenv('APPDATA')+"\\Macro Deck\\profiles.db"
db=sqlite3.connect(dbpath)
cur=db.cursor()
result=cur.execute("SELECT * FROM sqlite_master where type='table'").fetchall()
if len(result)!=1:
    raise Exception("Only one table is expected. Unknown tables found: "+str(result))
tablename=result[0][1]
result=cur.execute("INSERT INTO "+tablename+" VALUES ('"+profileoutput+"')").fetchall()
print(result)
db.commit()
print("Finished")
