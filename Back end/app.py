#no cmd instalar
# pip install opencv-python numpy matplotlib flask flask-cors


from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)# Adicione esta linha para habilitar CORS

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

if __name__ == '__main__':
    app.run(debug=True)