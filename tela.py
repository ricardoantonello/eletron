#https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

import tkinter as tk
from tkinter import filedialog, messagebox
import rrTkinterLib as rr # biblioteca personalizada de interface
from PIL import Image, ImageTk
import cv2 as cv

class AboutWindow(tk.Frame): # aqui teremos os widgets da tela
    def __init__(self, master=None): 
        super().__init__(master)
        self.master = master
        self.pack() # tipo do layout
        self.master.title('Sobre o projeto...')

        temp = 'INSTITUTO FEDERAL CATARINENSE - IFC\nCampus Luzerna\n\n\n\
Medição da carga contida nos elétrons por visão computacional\n\n\n\
Autores:\n\
Madge Bianchi dos Santos (madge.santos@ifc.edu.br)\n\
Ricardo Antonello (ricardo@antonello.com.br)\n\
Thiago Tavares (thiagotavares1997@gmail.com)\n\n\n\
Este trabalho é a implementação do "Experimento da Gota de Óleo de Millikan"'
        self.textoPrincipal = tk.Label(self, text=temp)
        #self.textoPrincipal.pack(side="top")
        self.textoPrincipal.pack(pady=50, padx=50)
        self.quit = rr.Button(self, text="Sair", command=self.master.destroy)
        self.quit.focus_force()
        self.quit.pack(side="bottom", pady=30, padx=30) # left, right, bottom, top
        
        
class MainWindow(tk.Frame): # aqui teremos os widgets da tela
    def __init__(self, toplevel): 
        super().__init__(toplevel)
        self.master = toplevel
        self.grid() # tipo do layout
        #self.master.maxsize(width=1920, height=1080)
        #self.master.minsize(width=640, height=480)
        self.master['bg']='white'
        #master.resizable(width=False, height=False)
        self.master.title('Medição da carga contida nos elétrons por visão computacional')
        self.create_widgets() 

    def create_widgets(self): 
        # CRIACAO DO MENU
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Abrir vídeo", command=self.openVideo)
        fileMenu.add_command(label="Usar câmera", command=self.openVideo)
        fileMenu.add_separator()
        fileMenu.add_command(label="Sair", command=root.quit)
        menubar.add_cascade(label="Arquivo", menu=fileMenu)
        helpMenu = tk.Menu(menubar, tearoff=0)
        helpMenu.add_command(label="Ajuda", command=self.openAbout)
        helpMenu.add_command(label="Sobre...", command=self.openAbout)
        menubar.add_cascade(label="Ajuda", menu=helpMenu)
        # FIM DA CRIACAO DO MENU

        logo = Image.open('ifc_logo.png')
        logo_width, logo_height = logo.size
        logo = logo.resize((logo_width//2, logo_height//2), Image.ANTIALIAS) #The (250, 250) is (height, width)
        logo = ImageTk.PhotoImage(logo)
        self.lb_img = tk.Label(self.master, image=logo)
        self.lb_img['borderwidth'] = 0
        self.lb_img.photo = logo
        self.lb_img.grid(column=1, row=1, sticky='n', rowspan=1, columnspan=2, padx=1, pady=1)
        
        self.lb1 = rr.Label(self.master)
        self.lb1["text"] = "Medição da carga \ncontida nos elétrons \npor visão computacional"
        self.lb1['bg']='white'
        self.lb1.grid(column=1, row=2, sticky='N', padx=1, pady=1)

        self.abrirVideo = rr.Button(self.master)
        self.abrirVideo["text"] = "Abrir Vídeo"
        self.abrirVideo["command"] = self.openVideo 
        self.abrirVideo.grid(column=1, row=3, sticky='N', padx=1, pady=1)

        self.abrirCamera = rr.Button(self.master)
        self.abrirCamera["text"] = "Usar Câmera"
        self.abrirCamera["command"] = self.openCamera
        self.abrirCamera.grid(column=1, row=4, sticky='N', padx=1, pady=1)

        self.about = rr.Button(self.master)
        self.about["text"] = "Autores"
        self.about["command"] = self.openAbout 
        self.about.grid(column=1, row=5, sticky='N', padx=1, pady=1)

        self.quit = rr.Button(self.master, text="Sair", command=self.master.destroy)
        self.quit.grid(column=1, row=6, sticky='S', padx=1, pady=1)
        self.quit.focus_force()

    def atualizaImagem(self):
        img = Image.open('ifc_logo.png')
        img_width, img_height = img.size
        #logo = logo.resize((logo_width//2, logo_height//2), Image.ANTIALIAS) #The (250, 250) is (height, width)
        img = ImageTk.PhotoImage(img)
        
        self.canvas = tk.Canvas(self.master, width=img_width, height=img_height, bg='white')
        self.canvas['borderwidth']=0
        self.canvas.grid(column=3, row=1, rowspan=4, padx=1, pady=1)
        tk.Label().photo = img  # bug: a imagem estar num label qualquer para aparecer no canvas 
        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=img, anchor=tk.NW, tag='img1')
    
    def openAbout(self):
        aboutWindow = AboutWindow(master=tk.Tk()) 
        aboutWindow.mainloop() 

    def openCamera(self):
        messagebox.showinfo("Em construção", "Utilização da câmera ainda não foi implementada.")

    def openVideo(self):
        ftypes = [('Vídeos mp4', '*.mp4'), ('All files', '*')]
        path = tk.filedialog.askopenfilename(filetypes=ftypes)
        if path != '':
            print(path)
# Load an image using OpenCV
        cv_img = cv.imread("teste.png")
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = cv_img.shape
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                    
    
    
root = tk.Tk() # biblioteca TK permite que os widgets sejam usados
app = MainWindow(root) # app será a tela principal da aplicação 
app.mainloop() # chama loop principal que fica lendo os eventos (como click de um botao)
