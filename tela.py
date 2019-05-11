#https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

import tkinter as tk

class Application(tk.Frame): # aqui teremos os widgets da tela
    def __init__(self, master=None): 
        super().__init__(master)
        self.master = master
        self.pack() # tipo do layout
        self.create_widgets() 

    def create_widgets(self): 
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")


        self.widget1 = tk.Frame(self.master)
        self.widget1.pack()
        self.msg = tk.Label(self.widget1, text="Primeiro widget")
        self.msg["font"] = ("Calibri", "9", "italic")
        self.msg.pack ()
        self.sair = tk.Button(self.widget1)
        self.sair["text"] = "Clique aqui"
        self.sair["font"] = ("Calibri", "9")
        self.sair["width"] = 10
        self.sair["command"] = self.mudarTexto
        self.sair.pack ()
  
    def mudarTexto(self):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"
        else:
            self.msg["text"] = "Primeiro widget"


    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk() # biblioteca TK permite que os widgets sejam usados
app = Application(master=root) # app será a tela principal da aplicação 
app.mainloop() # chama loop principal que fica lendo os eventos (como click de um botao)