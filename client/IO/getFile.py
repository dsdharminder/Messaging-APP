import tkinter
from tkinter import filedialog

# Find and return the location of a file via Tkinter UI
def GetFile():
	#tkinter.withdraw()
	filename = filedialog.askopenfilename()
	return filename
