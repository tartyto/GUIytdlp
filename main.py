from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import os
import sys
import pyperclip

v = Tk()
v.title("ultimate yt downloader")

WIDTH = 700
HEIGHT = 300

v.geometry(f"{WIDTH}x{HEIGHT}")
v.resizable(False,False)

v.columnconfigure(0,weight=1)
v.rowconfigure(2, weight=1)

saveFilePath = "saveData.json"

currentPath = os.path.dirname(sys.argv[0])
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

v.mainloop()