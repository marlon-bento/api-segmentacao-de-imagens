#no cmd instalar
# pip install opencv-python numpy matplotlib


import cv2 #OpenCV
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk, filedialog

def carregar_imagem():
    root = Tk()
    root.withdraw()  # Esconde a janela principal

    # Abre o diálogo de seleção de arquivo
    caminho_da_imagem = filedialog.askopenfilename()

    # Verifica se o usuário selecionou um arquivo
    if caminho_da_imagem:
        print(f'Caminho da Imagem: {caminho_da_imagem}')  # Adicione esta linha
        try:
            # Carrega a imagem usando o OpenCV com tratamento de codificação
            with open(caminho_da_imagem, 'rb') as f:
                byte_content = f.read()
            np_array = np.frombuffer(byte_content, dtype=np.uint8)
            imagem = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # Verifica se a imagem foi carregada com sucesso
            if imagem is not None:
                # Retorna a imagem para a função chamadora
                return imagem
            else:
                print("Não foi possível carregar a imagem. Verifique o formato do arquivo.")
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

# Chama a função e armazena a imagem retornada em 'imagem_carregada'
imagem_carregada = carregar_imagem()

plt.imshow(cv2.cvtColor(imagem_carregada, cv2.COLOR_BGR2RGB))
plt.show()

# Converter a imagem para escala de cinza
gray = cv2.cvtColor(imagem_carregada, cv2.COLOR_BGR2GRAY)

plt.subplot(131), plt.imshow(imagem_carregada[:, :, ::-1]), plt.title('Original')
plt.subplot(132), plt.imshow(imagem_carregada[:, :, ::1]), plt.title('bgr')
plt.subplot(133), plt.imshow(gray, cmap='gray'), plt.title('tom cinza')
# Mostre a figura
plt.show()










@app.route('/limiarizacao', methods=['POST'])
def processar_imagem():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)
        
        # Processar a imagem (converter para preto e branco)
        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        limiar = 160 #0 até 255

        val, thresh = cv2.threshold(img_gray,limiar,255, cv2.THRESH_BINARY) # (imagem, limiar, maximo, tipo de algoritimo)




        # Codificar ambas as imagens para base64
        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, img_gray_codificada = cv2.imencode('.png', img_gray)  # Adicione o _
        _, imagem_thresh_codificada = cv2.imencode('.png', thresh)


        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(imagem_thresh_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_pb': img_gray_base64,
            'imagem_thresh': imagem_thresh_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500







@app.route('/limiarizacao', methods=['POST'])
def limiarizacao():
    try:
        # Obter a imagem a partir dos dados POST
        dados_imagem = request.json['imagem']
        imagem_decodificada = base64.b64decode(dados_imagem)
        imagem_np = np.frombuffer(imagem_decodificada, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)
        
        # Processar a imagem (converter para preto e branco)
        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        limiar = 160 #0 até 255

        val, thresh = cv2.threshold(img_gray,limiar,255, cv2.THRESH_BINARY) # (imagem, limiar, maximo, tipo de algoritimo)




        # Codificar ambas as imagens para base64
        _, imagem_original_codificada = cv2.imencode('.png', imagem)
        _, img_gray_codificada = cv2.imencode('.png', img_gray)  # Adicione o _
        _, imagem_thresh_codificada = cv2.imencode('.png', thresh)


        imagem_original_base64 = base64.b64encode(imagem_original_codificada).decode('utf-8')
        img_gray_base64 = base64.b64encode(img_gray_codificada).decode('utf-8')
        imagem_thresh_base64 = base64.b64encode(imagem_thresh_codificada).decode('utf-8')

        # Retornar ambas as imagens processadas
        return jsonify({
            'imagem_original': imagem_original_base64,
            'imagem_pb': img_gray_base64,
            'imagem_thresh': imagem_thresh_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500