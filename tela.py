#https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

import tkinter as tk
from tkinter import filedialog, messagebox
import rrTkinterLib as rr # biblioteca personalizada de interface
from PIL import Image, ImageTk
import cv2 as cv
import visao

import numpy as np

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
        fileMenu.add_command(label="Usar câmera", command=self.openCamera)
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

    def openAbout(self):
        aboutWindow = AboutWindow(master=tk.Tk()) 
        aboutWindow.mainloop() 

    def openCamera(self):
        messagebox.showinfo("Em construção", "Utilização da câmera ainda não foi implementada.")

    def openVideo(self):
        ftypes = [('Vídeos mp4', '*.mp4'), ('All files', '*')]
        path = tk.filedialog.askopenfilename(filetypes=ftypes)
        if path == '':
            return
        print(path)
        print("Iniciando, por favor aguarde...")
        vc = visao.VideoCamera(tipo_fonte='video', arquivo=path)
        engine = visao.Engine()

        # Seta ROI (Region of Interest)
        messagebox.showinfo("Atenção", "Selecione a área de interesse e pressione [Enter].")
        success, frame = vc.get_frame()
        if not success:
            print('!! Erro acessando fonte de dados')
        roi = cv.selectROI(frame[::2,::2]) #diminui a imagem para escolher regiao de interesse
        #print('>> ROI:', roi)
        roi = (roi[0]*2, roi[1]*2, roi[2]*2, roi[3]*2)
        #print('>> ROI:', roi)
        #roi = (851, 402, 750, 470) #utilizado apenas para testes
        
        #Cria Canvas
        frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        img_width, img_height = frame.shape[1], frame.shape[0] 
        print('Shape:', img_width, img_height)
        #logo = logo.resize((logo_width//2, logo_height//2), Image.ANTIALIAS) #The (250, 250) is (height, width)
        frame = ImageTk.PhotoImage(frame)
        self.canvas = tk.Canvas(self.master, width=img_width, height=img_height, bg='white')
        self.canvas['borderwidth']=0
        self.canvas.grid(column=3, row=1, rowspan=5, padx=1, pady=1)
        tk.Label().photo = frame  # bug: a imagem estar num label qualquer para aparecer no canvas 
        self.canvas.create_image(0, 0, image=frame, anchor=tk.NW, tag='nao usado')

        while(1):
            success, frame = vc.get_frame()
            if not success:
                break
            # Recorta (crop) regiao selecionada
            frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            # Aplic filtros para melhorar a imagem
            frame_eq = visao.filtro_1(frame)
            frame_1 = engine.run_frame(frame)
            frame_2 = engine.run_frame(visao.filtro_2(frame))
            visao.escreve(frame_eq, 'Equalizado')
            visao.escreve(frame_1, 'Filtro 1')
            visao.escreve(frame_2, 'Filtro 2')
            visao.escreve(frame, 'Original')

            # Load an image using OpenCV
            cv_img = cv.imread("teste.png")
            # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
            height, width, no_channels = cv_img.shape
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            photo = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
        

            saida = np.vstack([np.hstack([frame, frame_eq]),np.hstack([frame_1, frame_2])])
            
            
            cv.imshow("Millikan Carga do Eletron # Autores: Madge Bianchi dos Santos, Ricardo Antonello e Thiago Tavares", saida)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()
        print('>> Resultados:')
        print('Velocidade média:', 33)
        print('>> Fim!')
    
root = tk.Tk() # biblioteca TK permite que os widgets sejam usados
app = MainWindow(root) # app será a tela principal da aplicação 
app.mainloop() # chama loop principal que fica lendo os eventos (como click de um botao)
