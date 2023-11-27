
document.getElementById('inputImagem-sobel').addEventListener('change', function() {
    var inputImagem = document.getElementById('inputImagem-sobel');
    var imagem = inputImagem.files[0];

    var reader = new FileReader();
    reader.onload = function (e) {
        var dadosImagem = e.target.result.split(',')[1];
       

        // Exibir mensagem de carregamento
        document.getElementById('processamento').innerHTML = 'Processando imagem...';
        document.getElementById('resultado').innerHTML = '';
        // Enviar imagem para a API
        $.ajax({
            url: 'http://127.0.0.1:5000/sobel',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'imagem': dadosImagem }),
            success: function (data) {
                document.getElementById('processamento').innerHTML = "<h1>Etapas de Processamento da imagem:</h1>"
                // Exibir imagem original
                document.getElementById('processamento').innerHTML +=` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_original}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem original</h1>
                </div>`
                // Exibir imagem processada (preto e branco)
                document.getElementById('processamento').innerHTML += ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_gray}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Imagem cinza</h1>
                </div>`
                
                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_canny}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Canny</h1>
                </div>`

                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_limiarizacao}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Limiarização</h1>
                </div>`

                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_sobel}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Sobel x e y</h1>
                </div>`

                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_soma}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Soma das seguimentações</h1>
                </div>`

                document.getElementById('resultado').innerHTML = "<h1>Resultado final:</h1>"

                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('resultado').innerHTML +=  ` 
                <div class="col text-center">          
                    <img id="minhaImagem" src="data:image/png;base64, ${data.resultado}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">resultado</h1>
                </div>`
                document.getElementById('resultado').innerHTML+=` 
                <label class="btn btn-primary btn-custom" for="inviteFundo">Envie a imagem que irá ficar de fundo</label>
                <input class="d-none" type="file" name="inviteFundo" id="inviteFundo"onchange="processImage()" accept="image/*"> 

                <button onclick="downloadImagem('minhaImagem')" class="btn btn-primary m-3">Baixar imagem</button>
                
                `

            },
            error: function (error) {
                console.log('Erro ao processar imagem:', error);
                document.getElementById('processamento').innerHTML = 'Erro ao processar imagem.';
            }
        });
        
    };
    
    reader.readAsDataURL(imagem);
    // Limpar o valor do campo de entrada de imagem
    inputImagem.value = null; // Use null para garantir a limpeza em diferentes navegadores

});

function downloadImagem(id) {

// Selecionar a tag <img> pelo ID
var imgTag = document.getElementById(id);

// Criar um link <a> temporário
var link = document.createElement('a');

// Configurar o link com o URL da imagem atual e o nome do arquivo desejado
link.href = imgTag.src;
link.download = 'nome_da_imagem.jpg'; // Substitua 'nome_da_imagem' pelo nome desejado

// Adicionar o link ao corpo do documento
document.body.appendChild(link);

// Simular um clique no link para iniciar o download
link.click();

// Remover o link do corpo do documento
document.body.removeChild(link);
}


function enviarImagens() {
    // Obtendo a imagem da tag com id minhaImagem
    var imagemMinhaImagem = $("#minhaImagem").attr("src");

    // Obtendo a imagem do input com id inviteFundo
    var inputInviteFundo = document.getElementById("inviteFundo");

    if (inputInviteFundo.files && inputInviteFundo.files[0]) {
        var leitor = new FileReader();

        leitor.onload = function(e) {
            var imagemInviteFundo = e.target.result;

            // Aqui você pode enviar as imagens para a sua API Flask usando AJAX
            enviarImagensParaAPI(imagemMinhaImagem, imagemInviteFundo);
        }

        leitor.readAsDataURL(inputInviteFundo.files[0]);
    }
}

function processImage() {
    const inputElement = document.getElementById("inviteFundo");
    const inputImageElement = document.getElementById("minhaImagem");

    const file = inputElement.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const imageData = e.target.result.split(',')[1];

        // Exibir mensagem de carregamento
        document.getElementById('processamento').innerHTML = 'Processando imagem...';
        document.getElementById('resultado').innerHTML = '';

        // Enviar ambas as imagens para a API usando $.ajax
        $.ajax({
            url: 'http://127.0.0.1:5000/process_images',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'input_image': imageData, 'tag_image': inputImageElement.src.split(',')[1] }),
            success: function (data) {
                document.getElementById('processamento').innerHTML = "<h1>Imagens:</h1>"
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img id="inputGrayscaleImage" src="data:image/png;base64, ${data.imagem_sem_fundo}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Imagem sem segmentada</h1>
                </div>`
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img id="tagGrayscaleImage" src="data:image/png;base64, ${data.novo_fundo}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">novo fundo</h1>
                </div>`
                document.getElementById('resultado').innerHTML = "<h1>Resultado final:</h1>"
                document.getElementById('resultado').innerHTML +=  ` 
                <div class="col text-center">          
                    <img id="fundoTrocado" src="data:image/png;base64, ${data.trocado}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">resultado</h1>
                </div>`
                document.getElementById('resultado').innerHTML+=` 

                <button onclick="downloadImagem('fundoTrocado')" class="btn btn-primary m-3">Baixar imagem</button>
                
                `
                
            },
            error: function (error) {
                console.log('Erro ao processar imagem:', error);
                document.getElementById('processamento').innerHTML = 'Erro ao processar imagem.';
            }
        });
    };

    reader.readAsDataURL(file);
    // Limpar o valor do campo de entrada de imagem
    inputElement.value = null; // Use null para garantir a limpeza em diferentes navegadores
}