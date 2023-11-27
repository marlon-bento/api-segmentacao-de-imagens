// script.js
$('#theForm').submit((e) => {
    e.preventDefault();
    var inputImagem = $('#inputImagem')[0].files[0]; //Imagem alvo
    var inputFundo = $('#inputFundo')[0].files[0]; //Imagem fundo
    var op = $('#inputOp')[0].value;  // Operacao
    console.log('A operação é: ', op);
    var reader = new FileReader(); // Converte imagem para envio como json (mudar depois)
    reader.onload = function (e) {
        var dadosImagem = e.target.result.split(',')[1];

        // Exibir mensagem de carregamento
        document.getElementById('resultado').innerHTML = 'Processando imagem...';

        // Enviar imagem para a API
        $.ajax({
            url: 'http://127.0.0.1:5000/color_gray',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'imagem': dadosImagem }),
            success: function (data) {
                document.getElementById('resultado').innerHTML = "<h1>Etapas de Processamento da imagem:</h1>"
                // Exibir imagem original
                document.getElementById('resultado').innerHTML +=` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_original}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem original</h1>
                </div>`
                // Exibir imagem processada (preto e branco)
                document.getElementById('resultado').innerHTML += ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_pb}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem preto e branco</h1>
                </div>`
                
            },
            error: function (error) {
                console.log('Erro ao processar imagem:', error);
                document.getElementById('resultado').innerHTML = 'Erro ao processar imagem.';
            }
        });
        
    };

    reader.readAsDataURL(inputImagem);
    // Limpar o valor do campo de entrada de imagem
    //inputImagem.value = null; // Use null para garantir a limpeza em diferentes navegadores
});
 // Adicione um ouvinte de evento para o input de imagem
 document.getElementById('inputImagem-gray').addEventListener('change', function() {
    var inputImagem = document.getElementById('inputImagem-gray');
    var imagem = inputImagem.files[0];

    var reader = new FileReader();
    reader.onload = function (e) {
        var dadosImagem = e.target.result.split(',')[1];

        // Exibir mensagem de carregamento
        document.getElementById('resultado').innerHTML = 'Processando imagem...';

        // Enviar imagem para a API
        $.ajax({
            url: 'http://127.0.0.1:5000/color_gray',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'imagem': dadosImagem }),
            success: function (data) {
                document.getElementById('resultado').innerHTML = "<h1>Etapas de Processamento da imagem:</h1>"
                // Exibir imagem original
                document.getElementById('resultado').innerHTML +=` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_original}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem original</h1>
                </div>`
                // Exibir imagem processada (preto e branco)
                document.getElementById('resultado').innerHTML += ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_pb}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem preto e branco</h1>
                </div>`
                
            },
            error: function (error) {
                console.log('Erro ao processar imagem:', error);
                document.getElementById('resultado').innerHTML = 'Erro ao processar imagem.';
            }
        });
        
    };

    reader.readAsDataURL(imagem);
    // Limpar o valor do campo de entrada de imagem
    inputImagem.value = null; // Use null para garantir a limpeza em diferentes navegadores
});

document.getElementById('inputImagem-limiarizacao').addEventListener('change', function() {
    var inputImagem = document.getElementById('inputImagem-limiarizacao');
    var imagem = inputImagem.files[0];

    var reader = new FileReader();
    reader.onload = function (e) {
        var dadosImagem = e.target.result.split(',')[1];
       

        // Exibir mensagem de carregamento
        document.getElementById('resultado').innerHTML = 'Processando imagem...';

        // Enviar imagem para a API
        $.ajax({
            url: 'http://127.0.0.1:5000/limiarizacao',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'imagem': dadosImagem }),
            success: function (data) {
                document.getElementById('resultado').innerHTML = "<h1>Etapas de Processamento da imagem:</h1>"
                // Exibir imagem original
                document.getElementById('resultado').innerHTML +=` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_original}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem original</h1>
                </div>`
                // Exibir imagem processada (preto e branco)
                document.getElementById('resultado').innerHTML += ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_pb}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem preto e branco</h1>
                </div>`
                
                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('resultado').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_thresh}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">imagem limiarizada</h1>
                </div>`


            },
            error: function (error) {
                console.log('Erro ao processar imagem:', error);
                document.getElementById('resultado').innerHTML = 'Erro ao processar imagem.';
            }
        });
        
    };


    
    

    reader.readAsDataURL(imagem);
    // Limpar o valor do campo de entrada de imagem
    inputImagem.value = null; // Use null para garantir a limpeza em diferentes navegadores
});


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
                    <img src="data:image/png;base64, ${data.imagem_sobel_x}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Sobel X</h1>
                </div>`
                
                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_sobel_y}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Sobel Y</h1>
                </div>`

                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_soma_xy}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Sobel XY</h1>
                </div>`

                document.getElementById('resultado').innerHTML = "<h1>Resultado final:</h1>"

                // Exibir imagem limiarizada (preto e branco)
                document.getElementById('resultado').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.resultado}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Sobel XY</h1>
                </div>`


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
