#no cmd instalar
# pip install opencv-python numpy matplotlib flask flask-cors 
# pip install scipy



from scipy.ndimage import label, generate_binary_structure
from flask import Flask, request, jsonify, render_template
#from flask_cors import CORS
import cv2
import numpy as np
import base64
from matplotlib import pyplot as plt


app = Flask(__name__)
#CORS(app)# Adicione esta linha para habilitar CORS


@app.route('/', methods=['GET'])
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/color_gray', methods=['POST'])
def gray():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)





        # Processar a imagem (converter para preto e branco)
        imagem_pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Codificar ambas as imagens para base64
        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, imagem_pb_codificada = cv2.imencode('.png', imagem_pb )  # Adicione o _

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        imagem_pb_base64 = base64.b64encode(imagem_pb_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_pb': imagem_pb_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    
@app.route('/processar_imagem', methods=['POST'])
def processar_imagem():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)
        
        # Processar a imagem (converter para preto e branco)
        imagem_pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Codificar ambas as imagens para base64
        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, imagem_pb_codificada = cv2.imencode('.png', imagem_pb)  # Adicione o _

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        imagem_pb_base64 = base64.b64encode(imagem_pb_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_pb': imagem_pb_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500



def downscale_image(image, scale_factor):
    """
    Reduz a qualidade da imagem pelo fator de escala.
    """
    height, width = image.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

def upscale_image(image, scale_factor):
    """
    Aumenta a qualidade da imagem de volta ao tamanho original.
    """
    height, width = image.shape[:2]
    new_size = (int(width / scale_factor), int(height / scale_factor))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)


def preencher_vizinhanca(imagem, tamanho_vizinhanca):
    # Encontrar contornos na imagem
    contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma imagem preta do mesmo tamanho
    imagem_conectada = np.zeros_like(imagem)

    # Preencher a área entre os contornos
    cv2.drawContours(imagem_conectada, contornos, -1, 255, thickness=cv2.FILLED)

    return imagem_conectada


@app.route('/limiarizacao', methods=['POST'])
def limiarizacao():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)
        
        # Reduzir a qualidade para acelerar o processamento
        imagem = downscale_image(imagem, scale_factor=0.4)




        # Processar a imagem (converter para preto e branco)
        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        desfoque = cv2.GaussianBlur(img_gray,(7,7),0) #suavização
        equ = cv2.equalizeHist(desfoque) #equalização
        #plt.subplot(131), plt.imshow(desfoque, cmap='gray'), plt.title('tom cinza')
        #plt.subplot(132), plt.imshow(equ, cmap='gray'), plt.title('tom cinza')
        #plt.show()
        
        # esse _, é por que retorna o valor do limiar e como não irá usar o tracinho serve pra não guardar em nenhum lugar
        #_, thresh = cv2.threshold(desfoque,130,255, cv2.THRESH_BINARY_INV) # limiarização normal (imagem, limiar, maximo, tipo de algoritimo)
        #_, thresh = cv2.threshold(equ,0,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU ) # limiarização otsu (imagem, minimo, maximo, tipo de algoritimo, metodo de otsu)
        #thresh = cv2.adaptiveThreshold(desfoque,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 9 ) # limiarização adaptativa Média (imagem, máximo, metodo de média,tipo de limiarização, tamanho da vizinhança de pixeis, constante subtraida da média )
        thresh = cv2.adaptiveThreshold(equ,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5 ) # limiarização adaptativa gaussiana(imagem, máximo, metodo de gaussiana,tipo de limiarização, tamanho da vizinhança de pixeis, constante subtraida da média )
        kernel = np.ones((3,3), np.uint8) #kernel
        erosao = cv2.erode(thresh, kernel) #erosão
        dilatacao = cv2.dilate(erosao,kernel, iterations=7) #dilatação
        thresh = dilatacao


        #elementos = dilatacao.copy()
        #contornos, hierarquia = cv2.findContours(elementos, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #imagem = imagem.copy()
       # for cnt in contornos:
           # area = cv2.contourArea(cnt)
          #  if area >= 100:
         #       elipse = cv2.fitEllipse(cnt)
        #        cv2.ellipse(imagem, elipse, (0,255,0),3)
       # thresh = imagem.copy()
        # Codificar ambas as imagens para base64




        # Crie uma máscara onde as bordas são brancas
        #_, mascara = cv2.threshold(thresh, 240, 255, cv2.THRESH_BINARY)

        #imagem_segmentada = cv2.bitwise_and(imagem, imagem, mask=mascara)

                
        #thresh = imagem_segmentada






        # Encontrar contornos na imagem segmentada
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # Criar uma máscara preta
        mascara = np.zeros_like(img_gray)
        # Filtrar contornos por área mínima, aspect ratio e área do contorno
        min_contour_area = 40
        max_aspect_ratio = 300.0
        min_contour_size = 10000  # Ajuste conforme necessário

        valid_contours = [
            cnt for cnt in contours if (
                cv2.contourArea(cnt) > min_contour_area and
                (max_aspect_ratio >= (cv2.arcLength(cnt, True) ** 2) / (4 * np.pi * cv2.contourArea(cnt))) and
                cv2.contourArea(cnt) > min_contour_size
            )
        ]
        
        # Preencher a máscara com os contornos encontrados
        cv2.drawContours(mascara, valid_contours, -1, (255), thickness=cv2.FILLED)
        
        
 
        # Aplicar a máscara na imagem original
        result = cv2.bitwise_and(imagem, imagem, mask=mascara)
        #aumentando a qualidade novamente da imagem
        result = upscale_image(result, scale_factor=0.2)
        # Converta a imagem resultante para base64
        _, result_codificada = cv2.imencode('.png', result)
        resultado_base64 = base64.b64encode(result_codificada).decode('utf-8')













        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, img_gray_codificada = cv2.imencode('.png', mascara)  # Adicione o _
        _, imagem_thresh_codificada = cv2.imencode('.png', thresh)

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(imagem_thresh_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_pb': img_gray_base64,
            'imagem_thresh': resultado_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

@app.route('/sobel', methods=['POST'])
def sobel():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)


        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        desfoque = cv2.GaussianBlur(img_gray,(7,7),0) #suavização
        equ = cv2.equalizeHist(desfoque) #equalização

        
        sobel_x = cv2.Sobel(equ, cv2.CV_64F, 1,0, ksize = 3)
        sobel_y = cv2.Sobel(equ, cv2.CV_64F, 0,1, ksize = 3)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        sobel = cv2.addWeighted(src1 = sobel_x, alpha=5, src2 = sobel_y, beta = 5, gamma = 0)

        







      
        # Encontrar contornos na imagem segmentada
        contours, _ = cv2.findContours(sobel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Criar uma máscara preta
        mascara = np.zeros_like(img_gray)
        # Filtrar contornos por área mínima, aspect ratio e área do contorno
        min_contour_area = 870000
        max_aspect_ratio = 6.0
        min_contour_size = 10000  # Ajuste conforme necessário

        valid_contours = [
            cnt for cnt in contours if (
                cv2.contourArea(cnt) > min_contour_area and
                (max_aspect_ratio >= (cv2.arcLength(cnt, True) ** 2) / (4 * np.pi * cv2.contourArea(cnt))) and
                cv2.contourArea(cnt) > min_contour_size
            )
        ]

        # Preencher a máscara com os contornos encontrados
        cv2.drawContours(mascara, valid_contours, -1, (255), thickness=cv2.FILLED)
 
        # Aplicar a máscara na imagem original
        result = cv2.bitwise_and(imagem, imagem, mask=mascara)

        # Converta a imagem resultante para base64
        _, result_codificada = cv2.imencode('.png', result)
        resultado_base64 = base64.b64encode(result_codificada).decode('utf-8')










        _, imagem_original_codificada = cv2.imencode('.png', mascara)
        _, img_gray_codificada = cv2.imencode('.png', sobel_x)  # Adicione o _
        _, imagem_thresh_codificada = cv2.imencode('.png', sobel_y)
        _, img_sobelx_codificada = cv2.imencode('.png', sobel_x)
        _, img_sobely_codificada = cv2.imencode('.png', sobel_y)
        _, img_sobelxy_codificada = cv2.imencode('.png', sobel)
        _, img_resultado_codificada = cv2.imencode('.png', sobel_y)

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(imagem_thresh_codificada).decode('utf-8')
        imagem_sobelx_base64 = base64.b64encode(img_sobelx_codificada).decode('utf-8')
        imagem_sobely_base64 = base64.b64encode(img_sobely_codificada).decode('utf-8')
        imagem_sobelxy_base64 = base64.b64encode(img_sobelxy_codificada).decode('utf-8')
        imagem_resultado_base64 = base64.b64encode(img_resultado_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_sobel_x': imagem_sobelx_base64,
            'imagem_sobel_y': imagem_sobely_base64,
            'imagem_soma_xy': imagem_sobelxy_base64,
            'resultado': resultado_base64

        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500    

if __name__ == '__main__':
    app.run(debug=True)