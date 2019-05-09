import cv2 as cv
from time import time
import numpy as np


class VideoCamera(object): 

    def __init__(self, tipo_fonte=None, arquivo=''):
        self.tipo_fonte = tipo_fonte
        self.arquivo = arquivo
        self.video = None
        print('>> tipo_fonte: ', self.tipo_fonte)

        if self.tipo_fonte == 'camera':
          try: 
            cam_id=int(self.tipo_fonte)
            self.video = cv.VideoCapture(cam_id)
            print('>> VideoCamera USB (',cam_id,') acionada!')
          except ValueError:
            print('!! ERRO CAMERA USB')
        elif self.tipo_fonte == 'video':
          try:
            print('>> Acessando arquivo: ', self.arquivo)
            self.video = cv.VideoCapture(self.arquivo)
          except ValueError:
            print('!! ERRO ABRINDO ARQUIVO!')

    def __del__(self):
      try:
        self.video.release()
      except:
        print('VideoCamera.video não existe em DAO_Cameras')
  
    def get_frame(self): 
      success, frame = self.video.read()
      if success:
        return True, frame
      else:
        return False, frame;    

class Visao:
    
    def __init__(self):
        self.frame = None
        self.counters = []
        self.last_pixels = [] # em duas dimensoes acumula os pixels das ultimas X linhas 
        self.tamanho_media_movel = 3
        self.flag_contagem = []
        self.fgbg = cv.createBackgroundSubtractorMOG2()


    def run_frame(self, frame=None):
        #se não passar parametro fram então tenta ler o atual de DAO_Cameras
        self.frame = frame
        #self.frame_ant = frame # por enquanto não esta usando frame anterior...
        
        fgmask = self.fgbg.apply(self.frame)
        backtorgb = cv.cvtColor(fgmask,cv.COLOR_GRAY2RGB)
        
            

        saida = backtorgb 
        #cv.putText(saida, str(self.counters[i]), (7, 33), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 10, cv.LINE_AA)
        #cv.putText(saida, str(self.counters[i]), (7, 33), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv.LINE_AA)
        #self.frame[e.y:e.y+e.h,e.x:e.x+e.w] = saida
        #print(fgmask.shape)
        
        return saida

    def save(self, image_path, frame):
      print(image_path, frame.shape)
      cv.imwrite(image_path, frame)

def retira_bordas(frame, tamanho_borda):
    #tamanho da borda em percentual da imagem
    lin = int(frame.shape[0]*(tamanho_borda/100.0))
    col = int(frame.shape[1]*(tamanho_borda/100.0))
    return frame[lin:frame.shape[0]-lin, col:frame.shape[1]-col]

def filtros_exib(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame = cv.GaussianBlur(frame, (3, 3), 0)
    frame = cv.equalizeHist(frame)
    frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    return frame

def filtros_proc(frame):
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame = cv.blur(frame, (3, 3))
    #frame = cv.GaussianBlur(frame, (3, 3), 0)
    #frame = cv.medianBlur(frame, 3)
    #frame = cv.equalizeHist(frame)
    #frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    return frame



if __name__ == '__main__':
    print("Iniciando, por favor aguarde...")

#    visao = Visao(config=config_temp)
    vc = VideoCamera(tipo_fonte='video', arquivo='video1.mp4')
    visao = Visao()


    # Seta ROI (Region of Interest)
    #success, frame = vc.get_frame()
    #if not success:
    #    print('!! Erro acessando fonte de dados')
    #roi = cv.selectROI(frame)
    #print('>> ROI:', roi)
    roi = (851, 402, 750, 470)

    while(1):
        success, frame = vc.get_frame()
        if not success:
            break
        #frame = retira_bordas(frame, 15) # retira 10% das bordas da imagem

        # Recorta (crop) regiao selecionada
        frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        
        # Aplic filtros para melhorar a imagem
        frame_exib = filtros_exib(frame)

        frame_proc = visao.run_frame(filtros_proc(frame))
        
        saida = np.vstack([np.hstack([frame, frame_proc]),np.hstack([frame_exib, frame_proc])])
        cv.imshow("Electron # Autores: Ricardo Antonello e Thiago Tavares", saida)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    print('>> Resultados:')
    print('Velocidade média:', 33)
        
    print('>> Fim!')
