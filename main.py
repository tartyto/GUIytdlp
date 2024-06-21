from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import os
import sys
import requests

CurrentVersion = "0.2"

import urllib.request



def updateVersion():
    accept = messagebox.askyesno("Update", "update available, install?")
    if(accept):
        os.rename(sys.argv[0], "oldPythonDownloaderDELETEusedfornewinstall")
        os.remove(saveFilePath)
        response = requests.get("https://api.github.com/repos/tartyto/GUIytdlp/releases/latest")
        print(response.json()["name"])
        print()
        print(response.json()["assets"][0]["browser_download_url"])
        file = urllib.request.urlopen(response.json()["assets"][0]["browser_download_url"])
        with open(response.json()["assets"][0]["name"], "wb") as outputfile:
            outputfile.write(file.read())
        sys.exit(0)

hasPiperclip = False
try:
    import pyperclip
    hasPiperclip = True
except ImportError:
    hasPiperclip = False

WIDTH = 700
HEIGHT = 300

v = Tk()
v.title("ultimate downloader")

v.geometry(f"{WIDTH}x{HEIGHT}")
v.resizable(False,False)

v.columnconfigure(0,weight=1)
v.rowconfigure(2, weight=1)

saveFilePath = "pythonDownloaderSaveData.json"

currentPath = os.path.dirname(sys.argv[0])

if(os.path.exists("oldPythonDownloaderDELETEusedfornewinstall")):
    os.remove("oldPythonDownloaderDELETEusedfornewinstall")

if not(os.path.exists(saveFilePath)):
    newFileData = {
        "defaultPath" : currentPath
    }
    with open(saveFilePath, "w") as saveFile:
        saveFile.write(json.dumps(newFileData))

folderPath = ""

def readFolderPath():
    global folderPath
    with open(saveFilePath, "r") as saveFile:
        fileData = json.loads(saveFile.read())
    folderPath = fileData["defaultPath"]

def writeFolderPath(path):
    global folderPath
    folderPath = path

    with open(saveFilePath, "r") as saveFile:
        fileData = json.loads(saveFile.read())
    fileData["defaultPath"] = path
    with open(saveFilePath, "w") as saveFile:
        saveFile.write(json.dumps(fileData))

readFolderPath()

# region inputPanel
inputPanel = ttk.Labelframe(v, text="Input")

inputPanel.columnconfigure(1, weight=1)

urlVar = StringVar(value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

urlLabel = ttk.Label(inputPanel, text="URL: ")
urlLabel.grid(row=0, column=0)

urlEntry = ttk.Entry(inputPanel, textvariable=urlVar)
urlEntry.grid(row=0, column=1, sticky=EW)

def pasteUrl():
    urlVar.set(pyperclip.paste())

if(hasPiperclip):
    urlPaste = ttk.Button(inputPanel, text="Paste", command=pasteUrl)
    urlPaste.grid(row=0, column=2, sticky=EW)


inputPanel.grid(row=0, column=0, sticky=NSEW)
# endregion

downloadPanel = ttk.LabelFrame(v, text="Download")

downloadPanel.columnconfigure(1, weight=1)

folderVar = StringVar(value=folderPath)

folderLabel = ttk.Label(downloadPanel, text="Destination folder: ")
folderLabel.grid(row=0, column=0)

folderEntry = ttk.Entry(downloadPanel, textvariable=folderVar)
folderEntry["state"] = DISABLED
folderEntry.grid(row=0, column=1, sticky=EW)

def chooseNewFolder():
    folderPath = filedialog.askdirectory()
    writeFolderPath(folderPath)
    folderVar.set(folderPath)

import yt_dlp

def download():
    os.chdir(folderPath)

    ydl = yt_dlp.YoutubeDL()
    outputCode = ydl.download(urlVar.get())
    if(outputCode == 0):
        messagebox.showinfo(title="Download",message="Download successful")
    else:
        messagebox.showerror(title="Download", message="Error downloading")

    os.chdir(currentPath)

folderButton = ttk.Button(downloadPanel, text="Choose", command=chooseNewFolder)
folderButton.grid(row=0, column=2, sticky=EW)

downloadPanel.grid(row=1, column=0,sticky=NSEW)

downloadButton = ttk.Button(v, text="DOWNLOAD", command=download)
downloadButton.grid(row=2, column=0, sticky=NSEW)

with urllib.request.urlopen('https://raw.githubusercontent.com/tartyto/GUIytdlp/main/versionData') as f:
    version = f.read().decode('utf-8')
    print(version)
    if not(CurrentVersion == version.replace("\n", "")):
        updateVersion()

v.mainloop()
