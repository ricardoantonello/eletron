from tkinter import *
from rrTkinterLib import *

FONTE = ('Helvetica','14','bold')

class Passwords:
    def __init__(self,toplevel):
        self.frame1=Frame(toplevel)
        self.frame1.pack()
        self.frame2=Frame(toplevel)
        self.frame2.pack()
        self.frame3=Frame(toplevel)
        self.frame3.pack()
        self.frame4=Frame(toplevel,pady=10)
        self.frame4.pack()
        rr.Label(self.frame1,text='PASSWORDS').pack()
        rr.Label(self.frame2,text='Nome: ',width=8).pack(side=LEFT)
        self.nome=rr.Entry(self.frame2,width=10)
        self.nome.focus_force() # Para o foco começar neste campo
        self.nome.pack(side=LEFT)
        rr.Label(self.frame3,text='Senha: ',width=8).pack(side=LEFT)
        self.senha=rr.Entry(self.frame3,width=10,show='*')
        self.senha.pack(side=LEFT)
        self.confere=rr.Button(self.frame4, text='Conferir',command=self.conferir)
        self.confere.pack()
        self.msg=rr.Label(self.frame4,text='AGUARDANDO...')
        self.msg.pack()
    
    def conferir(self):
        NOME=self.nome.get()
        SENHA=self.senha.get()
        if NOME == SENHA:
            self.msg['text']='ACESSO PERMITIDO'
            self.msg['fg']='darkgreen'
        else:
            self.msg['text']='ACESSO NEGADO'
            self.msg['fg']='red'
            self.nome.focus_force()
instancia=Tk()
Passwords(instancia)
instancia.mainloop()
