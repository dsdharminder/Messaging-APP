import tkinter as tk

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.W+tk.E+tk.N+tk.S)
		self.createWidgets()

	def createWidgets(self):
		top=self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.recordButton = tk.Button(self, text='Record')
		self.quitButton.grid(column=0, row=0, sticky=tk.W+tk.S)
		self.recordButton.grid(column=1, row=0, sticky=tk.E+tk.S)

app = Application()
app.master.title('Sample application')
app.mainloop()
