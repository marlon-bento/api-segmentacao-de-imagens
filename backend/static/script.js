// script.js
const ENDPOINT = "http://127.0.0.1:5000/"; // Endpoint da API

$('#theForm').submit((e) => {
    e.preventDefault();
    $("#resultado").empty(); // limpa o conteúdo da div
    $("#processamento").empty();
    var inputImagem = $('#inputImagem')[0].files[0]; //Imagem alvo
    var inputFundo = $('#inputFundo')[0].files[0]; //Imagem fundo
    var formData = new FormData($('#theForm')[0]);

    // Mensagem de processamento
    $('#processamento').innerHTML = 'Processando a imagem...';
    $('#resultado').innerHTML = '';


    // Requisicao AJAX pelo jQuery
    $.ajax({
        type: "POST",
        url: ENDPOINT + "processar",
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            // Recebe o JSON resposta da API caso sucesso
            document.getElementById('resultado').innerHTML = "<h1>Resultado:</h1>";
            // Exibir imagem original
            document.getElementById('resultado').innerHTML +=` 
            <div class="col text-center">          
                <img src="data:image/png;base64, ${data.imagem_original}" alt="">
                <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Original</h1>
            </div>`;
            // Exibir imagem em escala de cinza
            document.getElementById('processamento').innerHTML += ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_gray}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Cinza</h1>
                </div>`;
            // Exibir imagem canny
            document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_canny}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Canny</h1>
                </div>`;
            // Exibir imagem limiarizada
            document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_limiarizacao}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Limiarização</h1>
                </div>`;
            // Exibir imagem sobelizada
            document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_sobel}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Segmentação Sobel x|y</h1>
                </div>`;
            // Exibir imagem somada
            document.getElementById('processamento').innerHTML +=  ` 
                <div class="col text-center">          
                    <img src="data:image/png;base64, ${data.imagem_soma}" alt="">
                    <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Soma das Operações</h1>
                </div>`;
            // Perfumaria
            //document.getElementById('resultado').innerHTML = "<h1>Resultado final:</h1>";
            // Exibir imagem processada
            document.getElementById('resultado').innerHTML += ` 
            <div class="col text-center">          
                <img src="data:image/png;base64, ${data.imagem_semfundo}" alt="">
                <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Sem Background</h1>
            </div>`;
            // Exibir imagem com o fundo
            document.getElementById('resultado').innerHTML += ` 
            <div class="col text-center">          
                <img id="minhaImagem" src="data:image/png;base64, ${data.resultado}" alt="">
                <h1 class="fs-2 p-2 bg-dark bg-opacity-50 text-info">Resultado Final</h1>
            </div>`;
            // Temporario Merge
            document.getElementById('resultado').innerHTML+=`  
                <button onclick="downloadImagem('minhaImagem')" class="btn btn-primary m-3">Download</button>
                `;
            
        },
        error: function (xhr,status,error) {
            // Recebe o JSON resposta caso erro
            console.log('Erro ao processar imagem:', xhr.responseJSON);
            document.getElementById('resultado').innerHTML = 'Erro ao processar imagem: <br>';
            document.getElementById('resultado').innerHTML += `<div class='erro-msg text-danger'>${xhr.responseJSON.erro}</div>`; //pega o erro do objeto
        }
    });
});

// OUTRAS FUNCOES
function downloadImagem(id) {

    // Selecionar a tag <img> pelo ID
    var imgTag = document.getElementById(id);
    
    // Criar um link <a> temp
    var link = document.createElement('a');
    
    // Configurar o link com o URL da imagem atual e o nome do arquivo desejado
    link.href = imgTag.src;
    link.download = 'bentrimagem.jpg';
    
    // Adicionar o link ao corpo do documento
    document.body.appendChild(link);
    
    // Simular um clique no link para iniciar o download
    link.click();
    
    // Remover o link do corpo do documento
    document.body.removeChild(link);
}
