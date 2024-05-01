from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk

import config as config

import pickledb
import random

def distance(a, b):
	'''Расстояние Левенштейна'''

	a = a.lower().replace(' ', '')
	b = b.lower().replace(' ', '')
	def rec (i, j):
		if i == 0 or j == 0:
			return max(i, j)
		elif a[i-1] == b[j-1]:
			return rec(i-1, j-1)
		else:
			return 1 + min(
				rec(i, j-1), 
				rec(i-1, j),
				rec(i-1, j-1)
				)
	x = max((len(a), len(b)))
	return round(((x - rec(len(a), len(b))) / x) * 100)

class Main(Tk):
	'''Класс основного окна'''

	TITLE = 'Программа тренажёр | DrSheep'
	ICON = 'main.ico'
	FILE = None
	WORDS = None
	WORD = None
	MARK = {
		'good': ('Правильно', "Отлично!"),
		'evil': ("Неправильно!", "Неверно",)
	}
	ALL = 0
	CORRECT_PERCENT = 80
	CORRECT = 0

	def __init__(self, *args, **kwargs):
		'''Инициализация'''
		super().__init__(*args, **kwargs)
		self.title(self.TITLE)
		try:
			self.iconbitmap(self.ICON)
		except:
			pass
		self.geometry('180x250')
		self.initGUI()
		self.initialization()

	def initialization(self):
		'''Инициализация базы данных'''

		sttgs = pickledb.load('settings.ini', False)
		if not sttgs.exists('file'):
			mb.showerror(
				self.TITLE, 
				'Файл настроек не найден!'
				)
			self.destroy()
			return
		self.FILE = sttgs.get('file')

		db = pickledb.load(self.FILE, True)
		if not db.exists('words'):
			self.WORDS = (("Пожалуйста, настройте базу данных!", ''),)
		else:
			self.WORDS = db.get('words')
		self.WORD = random.choice(self.WORDS)
		self.word['text'] = self.WORD[0]

	def wordHadler(self, enter):
		'''Обработка слов'''

		correct = distance(enter, self.WORD[1])
		self.WORD = random.choice(self.WORDS)
		self.word['text'] = self.WORD[0]
		self.word.update()
		return correct

	def open(self):
		'''Открытие другой базы данных'''

		file = fd.askopenfile(mode='r', title=self.TITLE)
		if not file:
			#mb.showerror(self.TITLE, 'Выберите файл!')
			return
		self.FILE = file.name
		sttgs = pickledb.load('settings.ini', False)
		sttgs.set('file', self.FILE )
		sttgs.dump()

		self.initialization()

	def __settingsHandler(self):
		'''Костыль для дочернего окна'''

		self.initialization()
		self.window.destroy()
		self.focus_set()
		self.ent.focus_set()

	def settings(self):
		'''Настройка базы данных'''

		self.window = config.Main(self.FILE) #.mainloop()
		self.window.grab_set()
		self.window.focus_set()
		self.window.protocol('WM_DELETE_WINDOW', self.__settingsHandler) 

	def create(self):
		'''Создание базы данных'''

		file = fd.asksaveasfilename( title=self.TITLE)
		if not file:
			#mb.showerror(self.TITLE, 'Выберите файл!')
			return
		self.FILE = file
		sttgs = pickledb.load('settings.ini', False)
		sttgs.set('file', self.FILE)
		sttgs.dump()

		self.initialization()

	def initGUI(self):
		'''Инициализация интерфейса'''

		#Верхнее меню
		self.menu = Menu(self)
		menu = Menu(self.menu, tearoff=0)
		menu.add_command(label='Открыть', command=self.open)
		menu.add_command(label='Создать', command=self.create)
		menu.add_command(label='Настройки', command=self.settings)
		self.menu.add_cascade(label='Файл', menu=menu)
		self.config(menu=self.menu)

		#Инициация виджетов
		self.prcnt = Label(text='100%')
		self.mark = Label(text='...')
		self.word = Label(
			text="...", 
			font=("Comic Sans MS", 20, "bold")
			)
		self.ent = ttk.Entry()
		self.btn = ttk.Button(text="Ввод")

		self.ent.bind("<Return>", self.__action)
		self.ent.focus_set()
		self.btn.bind("<Button-1>", self.__action)

		self.prcnt.pack(side=TOP, expand=0, fill=X)
		self.word.pack( expand=True, fill=BOTH, pady=15)
		self.mark.pack( expand=0, fill=X)
		self.ent.pack(side=LEFT, expand=True, fill=BOTH)
		self.btn.pack(side=RIGHT, expand=True, fill=BOTH)

	def __action(self, event):
		'''Обработка нажатия на кнопку'''

		text = self.ent.get()
		if not text: return
		self.ent.delete(0, END)
		self.ALL += 1
		correct = self.wordHadler(text)
		if correct > self.CORRECT_PERCENT:
			self.mark['text'] = random.choice(self.MARK['good'])
			self.CORRECT += 1
		else:
			self.mark['text'] = random.choice(self.MARK['evil'])
		self.prcnt['text'] = str(int(self.CORRECT/self.ALL*100))+'%'

if __name__=='__main__':
	Main().mainloop()