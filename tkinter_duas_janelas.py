# -*- coding: cp1252 -*-
from tkinter import *
class Nao_Redimensiona:
    def __init__(self,janela):
        janela.resizable(width=False, height=False)
        janela.title('Não redimensiona!')
        Canvas(janela, width=200, height=100, bg='moccasin').pack()
class Tamanhos_Limite:
    def __init__(self,janela):
        janela.maxsize(width=300, height=300)
        janela.minsize(width=50, height=50)
        janela.title('Tamanhos limitados!')
        Canvas(janela, width=200, height=100, bg='moccasin').pack()
inst1, inst2 = Tk(), Tk()
Nao_Redimensiona(inst1)
Tamanhos_Limite(inst2)
inst1.mainloop()
inst2.mainloop()