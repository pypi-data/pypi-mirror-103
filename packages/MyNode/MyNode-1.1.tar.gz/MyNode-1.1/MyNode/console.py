from os import system
import ctypes

def log(logunit):
	

	print(logunit)

def title(ctunit):

	system("title " + ctunit)

def helpmodules():
	loque = print("""

Ayuda:



Console:

log | Usage = console.log(parametros)
title | Usage = console.title(parametros)
helpmodules | Usage = console.helpmodules() # Sin parametros


		""")
	return loque