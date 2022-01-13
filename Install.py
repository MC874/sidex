from tkinter import *
from os.path import abspath, dirname
from subprocess import *
import tkinter.ttk as ttk
import tkinter as tk
import platform as p
import tkinter
import tkinter.messagebox as tkMessageBox
import subprocess, sys
import os

root = tk.Tk()
top = tk.Toplevel(root)

class MessageBox(object):
	def __init__(self, msg, b1, b2, parent, cbo, cboList):
		root = self.root = tkinter.Toplevel(parent)
		root.iconbitmap(resource_path('MCrev.ico'))
		root.title('Choose')
		root.geometry('100x100')
		root.resizable(False, False)
		root.grab_set()
		self.msg = str(msg)
		self.b1_return = True
		self.b2_return = False
		if isinstance(b1, tuple): b1, self.b1_return = b1
		if isinstance(b2, tuple): b2, self.b2_return = b2
		frm_1 = tkinter.Frame(root)
		frm_1.pack(ipadx=2, ipady=2)
		message = tkinter.Label(frm_1, text=self.msg)
		if cbo: message.pack(padx=8, pady=8)
		else: message.pack(padx=8, pady=20)
		if cbo:
			self.cbo = ttk.Combobox(frm_1, state="readonly", justify="center", values= cboList)
			self.cbo.pack()
			self.cbo.focus_set()
			self.cbo.current(0)
		frm_2 = tkinter.Frame(frm_1)
		frm_2.pack(padx=4, pady=4)
		btn_1 = tkinter.Button(frm_2, width=8, text=b1)
		btn_1['command'] = self.b1_action
		if cbo: btn_1.pack(side='left', padx=5)
		else: btn_1.pack(side='left', padx=10)
		if not cbo: btn_1.focus_set()
		btn_2 = tkinter.Button(frm_2, width=8, text=b2)
		btn_2['command'] = self.b2_action
		if cbo: btn_2.pack(side='left', padx=5)
		else: btn_2.pack(side='left', padx=10)
		btn_1.bind('<KeyPress-Return>', func=self.b1_action)
		btn_2.bind('<KeyPress-Return>', func=self.b2_action)
		root.update_idletasks()
		root.geometry("210x110+%d+%d" % (parent.winfo_rootx()+7,parent.winfo_rooty()+70))
		root.protocol("WM_DELETE_WINDOW", self.close_mod)
		root.deiconify()
	def b1_action(self, event=None):
		try: x = self.cbo.get()
		except AttributeError:
			self.returning = self.b1_return
			self.root.quit()
		else:
			if x:
				self.returning = x
				self.root.quit()
	def b2_action(self, event=None):
		self.returning = self.b2_return
		os.system('for /d %c in ("%USERPROFILE%\AppData\Local\Temp\_MEI*")do @rd/s/q "%c"')
		sys.exit()
		raise SystemExit(0)
	def close_mod(self):
		self.returning = ";`x`;"
		os.system('for /d %d in ("%USERPROFILE%\AppData\Local\Temp\_MEI*")do @rd/s/q "%d"')
		sys.exit()
		raise SystemExit(0)

def mbox(msg, b1, b2, parent, cbo=False, cboList=[]):
	msgbox = MessageBox(msg, b1, b2, parent, cbo, cboList)
	msgbox.root.mainloop()
	msgbox.root.destroy()
	return msgbox.returning

def syscmd(cmd, encoding=''):
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
		close_fds=True)
	p.wait()
	output = p.stdout.read()
	if len(output) > 1:
		if encoding: return output.decode(encoding)
		else: return output
	return p.returncode

def resource_path(relative_path):
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

def dev_mode():
	root.withdraw()
	prompt={}
	listItems=['Activate Developer Mode','Check Developer Mode','Go to Menu']
	prompt['ans']=mbox('Developer Mode',('OK','ok'),('Exit','exit'),root,cbo=True,cboList=listItems)
	ans=prompt['ans']
	if ans=='Activate Developer Mode':
		syscmd('@echo off && REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"')
		syscmd('@echo off && DISM /Online /Add-Capability /CapabilityName:Tools.DeveloperMode.Core~~~~0.0.1.0')
		syscmd('@echo off && reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowAllTrustedApps" /d "1"')
		syscmd('@echo off && for /d %e in ("%USERPROFILE%\AppData\Local\Temp\_MEI*")do cd "%e" && powershell.exe install.ps1"')
		dev_check()
	elif ans=='Check Developer Mode':
		syscmd('@echo off && %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -Command "show-windowsdeveloperlicenseregistration"')
		main_menu()
	else:
		main_menu()

def dev_check():
	root.withdraw()
	top.withdraw()
	tkMessageBox.showinfo('Activated!','Your Developer Mode has been turned on! A reboot/restart is required to apply the changes!',parent=top)
	prompt={}
	listItems=['Reboot System','Go to Menu']
	prompt['ans']=mbox('Developer Mode',('OK','ok'),('Exit','exit'),root,cbo=True,cboList=listItems)
	ans=prompt['ans']
	if ans=='Reboot System':
		syscmd('shutdown /r')
		sys.exit()
		raise SystemExit(0)
	else:
		main_menu()

def mcrax_install():
	try:
		top.iconbitmap(resource_path('MCrev.ico'))
		root.withdraw()
		top.withdraw()
		os.chdir(dirname(abspath(__file__)))
		syscmd(r'ren "AppxBlockMap.xml" "_AppxBlockMap.xml"')
		syscmd(r'ren "AppxSignature.p7x" "_AppxSignature.p7x"')
		syscmd(r'%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -Command "Add-AppxPackage -Path AppxManifest.xml -Register"')
		syscmd(r'ren "_AppxBlockMap.xml" "AppxBlockMap.xml"')
		syscmd(r'ren "_AppxSignature.p7x" "AppxSignature.p7x"')
		tkMessageBox.showinfo('Finish!','Minecraft Installed!', parent=top)
		main_menu()
	except Exception:
		main_menu()

def fixes():
	try:
		syscmd(r'ren "_AppxBlockMap.xml" "AppxBlockMap.xml"')
		syscmd(r'ren "_AppxSignature.p7x" "AppxSignature.p7x"')
		main_menu()
	except Exception:
		main_menu()

def main_menu():
	root.withdraw()
	prompt={}
	listItems=['Developer Mode','Install']
	prompt['ans']=mbox('Option',('OK','ok'),('Exit','exit'),root,cbo=True,cboList=listItems)
	ans=prompt['ans']
	if ans=='Developer Mode':
		dev_mode()
	else:
		mcrax_install()

root.withdraw()
top.withdraw()
tkMessageBox.showinfo('First Use','Before Installing, make sure Developer Mode already Enabled!', parent=top)
os.chdir(dirname(abspath(__file__)))
fixes()
	