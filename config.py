from tkinter import *
from tkinter import ttk
import pickledb

class Main(Tk):
	FILE = None
	WORDS = None
	ICON = 'main.ico'

	def __init__(self, file, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.FILE = file
		self.title('Программа тренажёр — Программа конфигурации | DrSheep')
		try:
			self.iconbitmap(self.ICON)
		except:
			pass
		self.initGUI()
		self.initDB()

	def initDB(self):
		self.db = pickledb.load(self.FILE, False)

		if not self.db.exists('words'):
			self.db.set('words', [])

		self.WORDS = self.db.get('words')
		self.initLB()

	def initLB(self):
		self.lb.delete(0, END)
		for word in self.WORDS:
			print(word)
			self.lb.insert(END, word[0])
		print('log end\n')

	def addDB(self, word, translate):
		self.WORDS.append((word, translate))
		self.db.set('words', self.WORDS)
		self.db.dump()
		self.initLB()


	def initGUI(self):
		self.lb = Listbox(self, )
		self.wrd = Entry(self, text='word')
		self.trn = Entry(self, )
		self.btn1 = Button(self, text='Insert')
		self.btn2 = Button(self, text='Delete')

		#self.lb.insert(0, 'aaa')
		self.wrd.bind('<Return>', self.add)
		self.trn.bind('<Return>', self.add)
		self.btn1.bind('<Button-1>', self.add)
		self.btn2.bind('<Button-1>', self.delete)
		self.wrd.focus_set()

		self.lb.pack(expand=1, fill=BOTH)
		self.wrd.pack(expand=0, fill=X)
		self.trn.pack(expand=0, fill=X)
		self.btn1.pack(side='left', expand=1, fill=X)
		self.btn2.pack(side='right', expand=1, fill=X)

	def add(self, event):
		wrd = self.wrd.get()
		trn = self.trn.get()
		self.wrd.delete(0, END)
		self.trn.delete(0, END)
		self.addDB(wrd, trn)

	def delete(self, event):
		selection = self.lb.curselection()[0]
		print(selection)
		self.WORDS.pop(selection)
		print(self.WORDS)
		self.db.dump()
		self.initLB()

		
if __name__=='__main__':
	Main('words.db').mainloop()