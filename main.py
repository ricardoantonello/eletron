import tkinter as tk
from tkinter import filedialog, messagebox
import rrTkinterLib as rr # biblioteca personalizada de interface
from PIL import Image, ImageTk
import cv2 as cv
import visao
import time
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
        self.grab_set()
    
    def __del__(self): 
        print('Janela Help destruída...')
        self.grab_release()
     
        
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
        fileMenu.add_command(label="Abrir vídeo", command=lambda:self.openVideo('arquivo'))
        fileMenu.add_command(label="Usar câmera", command=lambda:self.openVideo('camera'))
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
        self.lb_img.grid(column=1, row=1, sticky='n', rowspan=1, columnspan=1, padx=1, pady=1)
        
        self.lb1 = rr.Label(self.master)
        self.lb1["text"] = "Medição da carga \ncontida nos elétrons \npor visão computacional"
        self.lb1['bg']='white'
        self.lb1.grid(column=1, row=2, sticky='N', padx=1, pady=1)

        self.abrirVideo = rr.Button(self.master)
        self.abrirVideo["text"] = "Abrir Vídeo"
        self.abrirVideo["command"] = lambda:self.openVideo('arquivo')
        self.abrirVideo.grid(column=1, row=3, sticky='N', padx=1, pady=1)

        self.abrirCamera = rr.Button(self.master)
        self.abrirCamera["text"] = "Usar Câmera"
        self.abrirCamera["command"] = lambda:self.openVideo('camera')
        self.abrirCamera.grid(column=1, row=4, sticky='N', padx=1, pady=1)

        self.about = rr.Button(self.master)
        self.about["text"] = "Autores"
        self.about["command"] = self.openAbout 
        self.about.grid(column=1, row=5, sticky='N', padx=1, pady=1)

        self.quit = rr.Button(self.master, text="Sair", command=self.master.destroy)
        self.quit.grid(column=1, row=6, sticky='S', padx=1, pady=1)
        self.quit.focus_force()

        self.framesCount = rr.Label(self.master, text='')
        self.framesCount.grid(column=1, row=7)

        self.lbautores = rr.Label(self.master)
        self.lbautores["text"] = "Autores: Madge Bianchi dos Santos, Thiago Tavares e Ricardo Antonello."
        self.lbautores.grid(column=2, row=7, sticky='e', padx=2, pady=2, columnspan=2)



    def openAbout(self):
        #aboutWindow = AboutWindow(master=tk.Tk()) 
        #aboutWindow.mainloop() 
        self.aboutWindow = tk.Toplevel(self.master) 
        self.app = AboutWindow(self.aboutWindow) 

    def update(self):
        try:
            success, frame = self.vc.get_frame()
            if success:
                # Recorta (crop) regiao selecionada
                frame = frame[int(self.roi[1]):int(self.roi[1]+self.roi[3]), int(self.roi[0]):int(self.roi[0]+self.roi[2])]
                # Aplic filtros para melhorar a imagem
                frame_eq = visao.filtro_1(frame)
                frame_1 = self.engine.run_frame(frame)
                frame_2 = self.engine.run_frame(visao.filtro_2(frame))
                visao.escreve(frame_eq, 'Equalizado')
                visao.escreve(frame_1, 'Filtro 1')
                visao.escreve(frame_2, 'Filtro 2')
                visao.escreve(frame, 'Original')
                saida = np.vstack([np.hstack([frame, frame_eq]),np.hstack([frame_1, frame_2])])
                #Converte de OpenCV para formato Tkinter no canvas
                frame = cv.cvtColor(saida, cv.COLOR_BGR2RGB)
                frame = ImageTk.PhotoImage(image = Image.fromarray(frame))    
                self.canvas.photo = frame  # IMPORTANTE: Importante salvar na instancia do canvas em .photo ou qualquer outra propriedade (tipo .xxx) para permitir a exibição
                self.canvas.itemconfig(self.image_on_canvas, image=frame)
                self.frameCounter += 1
                if self.frameCount==0:
                    self.framesCount['text'] = 'Contador de frames: %d' % self.frameCounter
                else:
                    self.framesCount['text'] = 'Contador de frames: %d/%d' % (self.frameCounter, self.frameCount)
                if self.isUpdating == True:
                    self.master.after(self.delay, self.update)
        except:
            print('Fonte de dados ausente!')
        
        
    def openVideo(self, source):
        self.frameCounter = 0
        if source == 'arquivo':
            ftypes = [('Vídeos mp4', '*.mp4'), ('All files', '*')]
            path = tk.filedialog.askopenfilename(filetypes=ftypes)
            if path == '':
                return
            print('Arquivo escolhido:', path)
            print("Iniciando, por favor aguarde...")
            try:
                self.vc.release()
                self.isUpdating = False
                time.sleep(1)
                del self.vc
            except:
                print('Fonte de dados existente foi eliminada!')
            self.vc = visao.VideoCamera('video', path)
            #exibe FPS do vídeo
            fps = self.vc.video.get(cv.CAP_PROP_FPS)
            self.delay = int(1000//fps) #velocidade de atualização da tela, ou seja, captura de um novo frame
            print("FPS do vídeo em video.get(cv.CAP_PROP_FPS): {0}".format(fps))
            print("self.delay:", self.delay)
            self.frameCount = int(self.vc.video.get(cv.CAP_PROP_FRAME_COUNT))
            print("self.frameCount do vídeo:", self.frameCount)
        elif source == 'camera':
            try:
                self.vc.release()
                self.isUpdating = False
                time.sleep(1)
                del self.vc
            except:
                print('Fonte de dados existente foi eliminada!')
            self.vc = visao.VideoCamera('camera', 0)
            self.delay = 15 # para camera um delay de 15 deve ser suficiente
            self.frameCount=0
        self.engine = visao.Engine()
        success, frame = self.vc.get_frame()
        if success:
            # Seta ROI (Region of Interest)
            messagebox.showinfo("Atenção!", "Selecione a área de interesse para o processamento e pressione a tecla [Enter].")
            roi = cv.selectROI(frame[::2,::2]) #diminui a imagem para escolher regiao de interesse
            #print('>> ROI:', roi)
            self.roi = (roi[0]*2, roi[1]*2, roi[2]*2, roi[3]*2)
            #print('>> ROI:', roi)
            #roi = (851, 402, 750, 470) #utilizado apenas para testes
            cv.destroyAllWindows()
            #Cria Canvas
            frame = frame[int(self.roi[1]):int(self.roi[1]+self.roi[3]), int(self.roi[0]):int(self.roi[0]+self.roi[2])]
            img_width, img_height = frame.shape[1], frame.shape[0] 
            print('Shape:', img_width, img_height)
            
            try:
                self.canvas.delete("all")
                self.canvas.update()
                del self.canvas
            except:
                print('Canvas antigo eliminado!')
            self.canvas = tk.Canvas(self.master, width=img_width*2, height=img_height*2, bg='white')
            self.canvas['borderwidth']=0
            self.canvas.grid(column=3, row=1, rowspan=6, padx=1, pady=1)
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW)
            # chama método update() para atualizar frames na tela 
            self.isUpdating = True
            self.update()
        else:
            messagebox.showinfo("Erro acessando fonte de dados!", "Erro acessando fonte de dados: Caso seja um arquivo de vídeo confira se o arquivo não esta corrompido. Caso seja uma câmera, confira se ela esta ligada corretamente ao computador.")            
            print('!! Erro acessando fonte de dados')
        

root = tk.Tk() # biblioteca TK permite que os widgets sejam usados
app = MainWindow(root) # app será a tela principal da aplicação 
app.mainloop() # chama loop principal que fica lendo os eventos (como click de um botao)
