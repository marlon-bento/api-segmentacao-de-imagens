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
import io

from werkzeug.utils import secure_filename
import tempfile
import os

app = Flask(__name__)
#CORS(app)# Adicione esta linha para habilitar CORS

#Extensoes permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#Essa constante guarda a pasta onde estarao as imagens temporariamente
TEMP_FOLDER = os.path.join(app.root_path, 'temporarios')
os.makedirs(TEMP_FOLDER, exist_ok=True)




@app.route('/', methods=['GET'])
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/processar', methods=['POST'])
def processar():
    try:
        # Aqui ele verifica se existe o campo no request object se nao BAD REQUEST
        if 'inputImagem' not in request.files or 'inputFundo' not in request.files:
            return jsonify({'erro': 'Ambos arquivos devem ser enviados!'}), 400

        # Obtem a imagem e o fundo direto do request
        dados_imagem = request.files['inputImagem']
        dados_fundo = request.files['inputFundo']

        # Validacoes Necessarias Sobre o Tipo de Arquivo
        if dados_imagem.filename == '' or dados_fundo.filename == '':
            return jsonify({'erro': 'Ambos arquivos devem ser enviados!'}), 400

        if not (allowed_file(dados_imagem.filename) and allowed_file(dados_fundo.filename)):
            return jsonify({'erro': 'Tipo invalido de arquivo. Deve ser png, jpg, jpeg'}), 400


        #Caminho do arquivo temporario que representa a imagem e nao sera deletado quando fechado
        caminho = tempfile.NamedTemporaryFile(delete=False,dir=TEMP_FOLDER).name
        caminho_fundo = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_FOLDER).name

        #Salva
        dados_imagem.save(caminho)
        dados_fundo.save(caminho_fundo)

        #A imagem eh lida pelo cv
        imagem = cv2.imread(caminho)

        #Realiza o processamento
        
        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        desfoque = cv2.GaussianBlur(img_gray,(7,7),0) #suavização
        
        canny = cv2.Canny(desfoque ,80,120)
        canny = cv2.dilate(canny, np.ones((3,3),np.uint8),iterations=1)
        
        contornos, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mascara = np.zeros((imagem.shape[0], imagem.shape[1]),dtype = np.uint8)
        cv2.drawContours(mascara, contornos, -1, (255,255,255), thickness=cv2.FILLED)


        mascara = cv2.dilate(mascara, np.ones((3,3),np.uint8),iterations=7)
        mascara = cv2.erode(mascara,np.ones((3,3),np.uint8),iterations=7)

        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mascara = np.zeros((imagem.shape[0], imagem.shape[1]),dtype = np.uint8)
        cv2.drawContours(mascara, contornos, -1, (255,255,255), thickness=cv2.FILLED)
        mask_canny = mascara.copy()

        segundo = limiarizacao(imagem)
        terceiro = sobelzinho(imagem)

        soma = cv2.bitwise_or(mascara, cv2.bitwise_or(segundo, terceiro))
        result = cv2.dilate(soma, np.ones((3,3),np.uint8),iterations=7)
        result = cv2.erode(result, np.ones((3,3),np.uint8),iterations=7)
        result = cv2.dilate(result, np.ones((3,3),np.uint8),iterations=5)
        contornos, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mascara = np.zeros((imagem.shape[0], imagem.shape[1]),dtype = np.uint8)
        
        cv2.drawContours(mascara, contornos, -1, (255,255,255), thickness=cv2.FILLED)
        mascara = cv2.erode(mascara, np.ones((3,3),np.uint8),iterations=5)

        # Criar uma imagem com a máscara aplicada
        sem_fundo = cv2.bitwise_and(imagem, imagem, mask=mascara)

        # SUBSTITUICAO DE FUNDO

        # Obter a imagem que quer substituir
        fundo_novo = cv2.imread(caminho_fundo)

         # Certificando-se de que as imagens têm o mesmo tamanho
        fundo_novo = cv2.resize(fundo_novo, (sem_fundo.shape[1], sem_fundo.shape[0]))

        # Criando uma máscara para o objeto segmentado
        gray = cv2.cvtColor(sem_fundo, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Invertendo a máscara para obter o fundo
        mask_inv = cv2.bitwise_not(mask)

        # Substituindo o fundo preto pelo novo fundo
        foreground = cv2.bitwise_and(sem_fundo, sem_fundo, mask=mask)
        background = cv2.bitwise_and(fundo_novo, fundo_novo, mask=mask_inv)
        result = cv2.add(foreground, background)

        # TRANSFORMACAO EM JSON TEMPORARIA (mudar depois)

        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, img_gray_codificada = cv2.imencode('.png', img_gray)  # Adicione o _
        _, imagem_canny_codificada = cv2.imencode('.png', mask_canny)
        _, img_thresh_codificada = cv2.imencode('.png', segundo)
        _, img_sobel_codificada = cv2.imencode('.png', terceiro)
        _, img_soma_codificada = cv2.imencode('.png', mascara)
        _, img_semfundo_codificada = cv2.imencode('.png', sem_fundo)
        _, resultado_image_png = cv2.imencode('.png', result)
        

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_canny_base64 = base64.b64encode(imagem_canny_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(img_thresh_codificada).decode('utf-8')
        imagem_sobel_base64 = base64.b64encode(img_sobel_codificada).decode('utf-8')
        imagem_soma_base64 = base64.b64encode(img_soma_codificada).decode('utf-8')
        imagem_semfundo_base64 = base64.b64encode(img_semfundo_codificada).decode('utf-8')
        resultado_image_png_64 = base64.b64encode(resultado_image_png).decode('utf-8')


        # Deleta o caminho temporario e a imagem temporaria
        os.remove(caminho)
        os.remove(caminho_fundo)

        # Retornar as imagens processadas em formato JSON
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_gray': img_gray_base64,
            'imagem_canny': imagem_canny_base64,
            'imagem_limiarizacao': imagem_thresh_base64,
            'imagem_sobel': imagem_sobel_base64,
            'imagem_soma': imagem_soma_base64,
            'imagem_semfundo': imagem_semfundo_base64,
            'resultado': resultado_image_png_64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# REALIZA OPERACAO SOBEL
def sobelzinho(imagem):

    img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    #equ = cv2.equalizeHist(img_gray) #equalização
    desfoque = cv2.GaussianBlur(img_gray,(7,7),2) #suavização
    

    # Segunda maneira
    sobel_x = cv2.Sobel(desfoque, cv2.CV_64F, 1, 0, ksize = 1)
    sobel_y = cv2.Sobel(desfoque, cv2.CV_64F, 0, 1, ksize = 1)


    # Calcular a magnitude do gradiente
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalizar para valores entre 0 e 255 (opcional)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Converter para uint8
    magnitude = np.uint8(magnitude)
    
    magnitude = cv2.dilate(magnitude, np.ones((3,3),np.uint8),iterations=2)
    


    # Calcular o limiar ótimo usando Otsu's Thresholding
    _, binary_image = cv2.threshold(np.abs(magnitude), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontrar contornos na imagem segmentada
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma máscara preta
    mascara = np.zeros_like(img_gray)
    # Filtrar contornos por área mínima, aspect ratio e área do contorno
    min_contour_area = 20
    max_aspect_ratio = 2000.0
    min_contour_size = 20  # Ajuste conforme necessário

    valid_contours = [
        cnt for cnt in contours if (
            cv2.contourArea(cnt) > min_contour_area and
            (max_aspect_ratio >= (cv2.arcLength(cnt, True) ** 2) / (4 * np.pi * cv2.contourArea(cnt))) and
            cv2.contourArea(cnt) > min_contour_size
        )
    ]



    # Preencher a máscara com os contornos encontrados
    cv2.drawContours(mascara, valid_contours, -1, (255), thickness=cv2.FILLED)
    mascara = cv2.erode(mascara, np.ones((3,3),np.uint8),iterations=2) 
    
    return mascara

# REALIZA OPERACAO DE LIMIARIZACAO
def limiarizacao(imagem):

    img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(img_gray) #equalização
    desfoque = cv2.GaussianBlur(equ,(7,7),0) #suavização
    thresh = cv2.adaptiveThreshold(desfoque,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 3 ) # limiarização adaptativa Média (imagem, máximo, metodo de média,tipo de limiarização, tamanho da vizinhança de pixeis, constante subtraida da média )
    #thresh = cv2.adaptiveThreshold(desfoque,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3 ) # limiarização adaptativa gaussiana(imagem, máximo, metodo de gaussiana,tipo de limiarização, tamanho da vizinhança de pixeis, constante subtraida da média )
    




    thresh = cv2.erode(thresh,np.ones((3,3),np.uint8),iterations=2)
    



    # Encontrar contornos na imagem segmentada
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma máscara preta
    mascara = np.zeros_like(img_gray)
    # Filtrar contornos por área mínima, aspect ratio e área do contorno
    min_contour_area = 1200
    max_aspect_ratio = 1000.0
    min_contour_size = 150  # Ajuste conforme necessário

    valid_contours = [
        cnt for cnt in contours if (
            cv2.contourArea(cnt) > min_contour_area and
            (max_aspect_ratio >= (cv2.arcLength(cnt, True) ** 2) / (4 * np.pi * cv2.contourArea(cnt))) and
            cv2.contourArea(cnt) > min_contour_size
        )
    ]



    # Preencher a máscara com os contornos encontrados
    cv2.drawContours(mascara, valid_contours, -1, (255), thickness=cv2.FILLED)
    
    return mascara

# FUNCOES AUXILIARES
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def preencher_vizinhanca(imagem, tamanho_vizinhanca):
    # Encontrar contornos na imagem
    contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma imagem preta do mesmo tamanho
    imagem_conectada = np.zeros_like(imagem)

    # Preencher a área entre os contornos
    cv2.drawContours(imagem_conectada, contornos, -1, 255, thickness=cv2.FILLED)

    return imagem_conectada


# MAIN

if __name__ == '__main__':
    app.run(debug=True)