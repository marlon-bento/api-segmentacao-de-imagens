#no cmd instalar
# pip install opencv-python numpy matplotlib flask flask-cors 
# pip install scipy



from scipy.ndimage import label, generate_binary_structure
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from matplotlib import pyplot as plt


app = Flask(__name__)
CORS(app)# Adicione esta linha para habilitar CORS
    

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
        result_img = cv2.bitwise_and(imagem, imagem, mask=mascara)

        
        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, img_gray_codificada = cv2.imencode('.png', img_gray)  # Adicione o _
        _, imagem_canny_codificada = cv2.imencode('.png', mask_canny)
        _, img_thresh_codificada = cv2.imencode('.png', segundo)
        _, img_sobel_codificada = cv2.imencode('.png', terceiro)
        _, img_soma_codificada = cv2.imencode('.png', mascara)
        _, img_resultado_codificada = cv2.imencode('.png', result_img)

        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_canny_base64 = base64.b64encode(imagem_canny_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(img_thresh_codificada).decode('utf-8')
        imagem_sobel_base64 = base64.b64encode(img_sobel_codificada).decode('utf-8')
        imagem_soma_base64 = base64.b64encode(img_soma_codificada).decode('utf-8')
        imagem_resultado_base64 = base64.b64encode(img_resultado_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_gray': img_gray_base64,
            'imagem_canny': imagem_canny_base64,
            'imagem_limiarizacao': imagem_thresh_base64,
            'imagem_sobel': imagem_sobel_base64,
            'imagem_soma': imagem_soma_base64,
            'resultado': imagem_resultado_base64

        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500   


def convert_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

@app.route('/process_images', methods=['POST'])
def process_images():
    try:
        # Recebe os dados da requisição
        data = request.get_json()

        # Decodifica a imagem base64 do input
        input_image_data = base64.b64decode(data['input_image'])
        input_image_np = np.frombuffer(input_image_data, dtype=np.uint8)
        background_image = cv2.imdecode(input_image_np, cv2.IMREAD_COLOR)

        # Decodifica a imagem base64 da tag
        tag_image_data = base64.b64decode(data['tag_image'])
        tag_image_np = np.frombuffer(tag_image_data, dtype=np.uint8)
        foreground_image = cv2.imdecode(tag_image_np, cv2.IMREAD_COLOR)


        # Certificando-se de que as imagens têm o mesmo tamanho
        background_image = cv2.resize(background_image, (foreground_image.shape[1], foreground_image.shape[0]))

        # Criando uma máscara para o objeto segmentado
        gray = cv2.cvtColor(foreground_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Invertendo a máscara para obter o fundo
        mask_inv = cv2.bitwise_not(mask)

        # Substituindo o fundo preto pelo novo fundo
        foreground = cv2.bitwise_and(foreground_image, foreground_image, mask=mask)
        background = cv2.bitwise_and(background_image, background_image, mask=mask_inv)
        result = cv2.add(foreground, background)


        # Resposta em base64
        _, foreground_image_png = cv2.imencode('.png', foreground_image)
        foreground_image_png_64 = base64.b64encode(foreground_image_png).decode('utf-8')

        _, background_image_png = cv2.imencode('.png', background_image)
        background_image_png_64 = base64.b64encode(background_image_png).decode('utf-8')

        _, resultado_image_png = cv2.imencode('.png', result)
        resultado_image_png_64 = base64.b64encode(resultado_image_png).decode('utf-8')

        response = {
            'imagem_sem_fundo': foreground_image_png_64,
            'novo_fundo': background_image_png_64,
            'trocado': resultado_image_png_64 
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)