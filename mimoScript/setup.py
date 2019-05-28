# -*- coding: utf-8 -*
#!/usr/bin/env python3

from subprocess import Popen, PIPE

#   AppleScript代码
script = '''
set home to the path to home folder
set f to the POSIX path of home & "Desktop/mimoScript/read.txt"

set Str to read POSIX file f as «class utf8»

--相对路径，不可用，现在只能绝对路径
--set f to the (POSIX path of ((path to me as text) & "::") & "read.txt") as POSIX file
--set Str to read f as «class utf8»

--设置歌词
tell application "mimoLive" to activate
tell application "System Events"
	tell process "mimoLive"
		ignoring application responses
			repeat until window 1 exists
			end repeat
			tell window 1
				set value of text area 1 of scroll area 1 of group 1 of scroll area 1 of splitter group 1 of splitter group 1 to Str
			end tell
		end ignoring
	end tell
end tell

--回到python窗口
tell app "Finder" to set frontmost of process "Python" to true 
'''

lysics_choose = " "	#全局变量
song_name =" "
numT = "0"

import os
filePath = './songList'
song_list = os.listdir(filePath)	#	获取歌词文件列表

from tkinter import *
from tkinter import messagebox
from tkinter import StringVar
from tkinter import ttk


def set_window():   #   选歌词窗口
	root = Tk()
	root.title("选择歌词文件 ")
	
	#   获取选中歌词
	def get_lysics(*args):
		global lysics_choose
		lysics_choose = song_choose.get()

	#   写入content.txt
	def writeIn(*args):
		lysics_choose = song_choose.get()
		path = "songList/" + lysics_choose
		count_T = len(open(path, 'r').readlines())
		count_T = count_T - 1
		numT = 0
		while numT < count_T:
			if numT == 0:
				file = open(path, mode='r', encoding="utf-8")
				this_song = file.readlines()[int(numT)]
				#print(this_song)
				file = open('content.txt', mode='w+', encoding="utf-8")
				file.write(this_song)
				numT=numT+1
			else:
				file = open(path, mode='r', encoding="utf-8")
				this_song = file.readlines()[int(numT)]
				#print(this_song)
				file = open('content.txt', mode='a+', encoding="utf-8")
				file.write(this_song)
				numT=numT+1

		if numT == count_T:
			file = open(path, mode='r', encoding="utf-8")
			this_song = file.readlines()[int(count_T)].replace("\n", "")
			#print(this_song)
			file = open('content.txt', mode='a+', encoding="utf-8")
			file.write(this_song)
		
		file.close()
		root.destroy()  #   销毁窗口
		global song_name	#	设置歌名变量
		song_name.set('当前歌词：'+lysics_choose)

	#   设置窗口
	panelCombo = ttk.Frame( root )
	panelCombo.pack( side='top', fill='x', padx=12, pady=8 )
	song_choose = ttk.Combobox( panelCombo)
	song_choose.pack( side='left', anchor='w', padx=12, pady=8 )
	song_choose['value'] = song_list
	song_choose["state"] = "readonly"
	song_choose.current(0)
	song_choose.bind("<<ComboboxSelected>>", get_lysics)

	write_in_button = Button(panelCombo, text="确定", width = 4,height=2,command=writeIn)	#	确认按钮
	write_in_button.pack(side='left', anchor='w', padx=8, pady=8)

	root.attributes( '-topmost', 0 )
	root.mainloop()


class MY_GUI():
	def __init__(self,init_window_name):
		self.init_window_name = init_window_name
		self.init_window_name.bind("<space>", self.change_next_line)    #   设置下一行快捷键
		self.init_window_name.bind("p", self.change_previous_line)  #   设置上一行快捷键
	#设置窗口
	def set_init_window(self):
		self.num = 0    #定义读取行数
		self.contentVar = StringVar()   #当前行歌词显示变量
		self.contentVar.set("当前：")
		self.nextVar = StringVar()  #下一行歌词显示变量
		self.nextVar.set("下一句：")
		self.count_line = len(open('content.txt', 'r').readlines()) #定义总行数

		global song_name
		song_name = StringVar()
		song_name.set('当前歌词：')

		self.init_window_name.title("唱词插件V1.0 by:林嘉瑜")  #窗口名
		self.init_window_name.geometry('200x200+1000+100')     #290 160为窗口大小，+100 +100 定义窗口弹出时的默认展示位置
		self.init_window_name.resizable(0,0)    #固定窗口大小
		self.init_window_name["bg"] = "#f4f5fa"       #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
		self.init_window_name.attributes("-alpha",1)     #虚化，值越小虚化程度越高
		self.frame_root = Frame(self.init_window_name,bg="#f4f5fa")#最外层frame
		self.frame_root.grid(row=0,column=0,padx=4,pady=4,sticky="W")
		self.frame_lyrics = Frame(self.init_window_name,bg='#ffffff')#歌词框架
		self.frame_lyrics.grid(row=1,column=0,padx=4,pady=4,sticky="W")
		self.frame_choose = Frame(self.init_window_name,bg='white')#歌词框架
		self.frame_choose.grid(row=2,column=0,padx=4,pady=4,sticky="W")

		self.change_next_line_button = Button(self.frame_root,state=DISABLED,text="下一行",height=2,width=5,command= self.change_next_line ) # 下一行按钮
		self.change_next_line_button.grid(row=0,column=0)

		self.change_previous_line_button = Button(self.frame_root,state=DISABLED,text="上一行",height=2,width=5,command= self.change_previous_line ) # 上一行按钮
		self.change_previous_line_button.grid(row=0,column=1)

		self.change_start_button = Button(self.frame_root,text="开始",height=2,width=5,foreground="#2F80ED",command= self.change_start) # 开始按钮
		self.change_start_button.grid(row=0,column=2)

		self.restart_button = Button(self.frame_root,text="重置",height=2,width=5,foreground="#FF4961",command= self.restart) # 重置按钮
		self.restart_button.grid(row=0,column=3)

		self.show_current_line = Label(self.frame_lyrics,textvariable=self.contentVar,height=2,font=('YaHei', 10),foreground="#FF4961",bg="#ffffff")    # 当前行显示
		self.show_current_line.grid(row=2,column=0,columnspan=20,sticky=W,padx=4,pady=4)

		self.show_next_line = Label(self.frame_lyrics,textvariable=self.nextVar,height=2,font=('YaHei', 10),bg="#ffffff")  # 下一行显示
		self.show_next_line.grid(row=3,column=0,columnspan=20,sticky=W,padx=4,pady=4)

		self.song_choose_title = Button(self.frame_choose, text="选择歌词", height=2,font=('YaHei', 10),command= set_window)
		self.song_choose_title.grid(row=0,column=0,sticky=W,padx=4,pady=1)
		
		self.song_current_title = Label(self.frame_choose, textvariable=song_name, height=1,font=('YaHei', 10))
		self.song_current_title.grid(row=0,column=1,sticky=W,padx=4,pady=1)

	# 切换下一行
	def change_next_line(self, event=' '):
		self.num = self.num + 1

		if self.num == self.count_line - 1: #最后一行弹窗提示
			file = open('content.txt', mode='r', encoding="utf-8")   
			t = file.readlines()[self.num]
			file.close() 
			file = open('read.txt', mode='w+', encoding="utf-8")           
			file.write(t)
			file.close() # 关闭文件
			self.num = self.num - 1
			p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
			stdout, stderr = p.communicate(script)
			msg_box=messagebox.showwarning(parent=self.init_window_name,title='通知',message='已到最后一行，点击重置按钮返回第一行')

		else:    
			file = open('content.txt', mode='r', encoding="utf-8")   
			t = file.readlines()[self.num]
			file.close() 
			file = open('read.txt', mode='w+', encoding="utf-8")
			file.write(t)
			file.close() # 关闭文件
			#   文本显示
			self.contentVar.set("当前：" + t)
			file = open('content.txt', mode='r', encoding="utf-8")
			t = file.readlines()[self.num+1] 
			file.close() # 关闭文件
			self.nextVar.set("下一句：" + t)
			p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)    # 运行AppleScript
			stdout, stderr = p.communicate(script)
	
	#切换上一行
	def change_previous_line(self, event=' '):
		file = open('content.txt', mode='r', encoding="utf-8")
		t = file.readlines()[self.num] 
		file.close() # 关闭文件

		if self.num <= 0:   # 第一行提示
			self.num = 0
			file = open('content.txt', mode='r', encoding="utf-8")   
			t = file.readlines()[0]
			file.close() 
			file = open('read.txt', mode='w+', encoding="utf-8")
			file.write(t)
			file.close() # 关闭文件
			p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
			stdout, stderr = p.communicate(script) 
			msg_box=messagebox.showwarning(parent=self.init_window_name,title='通知',message='已是第一行')
			self.contentVar.set("当前：" + t ) 
			file = open('content.txt', mode='r', encoding="utf-8")
			t = file.readlines()[self.num+1] 
			file.close() # 关闭文件
			self.nextVar.set("下一句：" + t)

		else:  
			self.num = self.num - 1
			file = open('read.txt', mode='r', encoding="utf-8")
			t_check = file.read()
			file.close()
			file = open('content.txt', mode='r', encoding="utf-8")   
			t = file.readlines()[self.num]
			file.close() 

			if t == t_check:
				self.num = self.num - 1
				file = open('content.txt', mode='r', encoding="utf-8")   
				t = file.readlines()[self.num]
				file.close() 
				file = open('read.txt', mode='w+', encoding="utf-8")
				file.write(t)
				file.close() # 关闭文件
				self.contentVar.set("当前：" + t)
				file = open('content.txt', mode='r', encoding="utf-8")
				t = file.readlines()[self.num+1] 
				file.close() # 关闭文件
				self.nextVar.set("下一句：" + t)
				p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
				stdout, stderr = p.communicate(script)
			else:
				file = open('content.txt', mode='r', encoding="utf-8")   
				t = file.readlines()[self.num]
				file.close() 
				file = open('read.txt', mode='w+', encoding="utf-8")
				file.write(t)
				file.close() # 关闭文件
				self.contentVar.set("当前：" + t)
				file = open('content.txt', mode='r', encoding="utf-8")
				t = file.readlines()[self.num+1] 
				file.close() # 关闭文件
				self.nextVar.set("下一句：" + t)
				p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
				stdout, stderr = p.communicate(script)

	# 开始
	def change_start(self): 
		file = open('content.txt', mode='r', encoding="utf-8")
		t = file.readlines()[self.num]
		file.close()
		file = open('read.txt', mode='w+', encoding="utf-8")
		file.write(t)
		file.close() # 关闭文件

		self.contentVar.set("当前：" + t)
		file = open('content.txt', mode='r', encoding="utf-8")
		t = file.readlines()[self.num+1] 
		file.close() # 关闭文件
		self.nextVar.set("下一句：" + t)
		p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
		stdout, stderr = p.communicate(script)
		# 按钮状态更改
		self.change_start_button.configure(state='disable') 
		self.change_next_line_button.configure(state='normal')
		self.change_previous_line_button.configure(state='normal')
		self.count_line = len(open('content.txt', 'r').readlines())

	# 重置
	def restart(self):
		self.num = 0
		file = open('read.txt', mode='w+', encoding="utf-8")
		file.write(" ")
		file.close() # 关闭文件
		self.contentVar.set("当前：")
		self.nextVar.set("下一句：")
		p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
		stdout, stderr = p.communicate(script)
		# 按钮状态更改
		self.change_start_button.configure(state='normal') 
		self.change_next_line_button.configure(state='disable')
		self.change_previous_line_button.configure(state='disable')           

def gui_start():
		init_window = Tk()    #实例化出一个父窗口
		AAA_PORTAL = MY_GUI(init_window)
		# 设置根窗口默认属性
		AAA_PORTAL.set_init_window()
		init_window.attributes('-topmost', True)  # 固定窗口在最前
		init_window.mainloop()   #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
gui_start()
