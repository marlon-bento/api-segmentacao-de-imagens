
$(document).ready(function() {
    
    // Adicione um ouvinte de evento para o link

    $("#click-sobel").click(function() {
        mostrarSobel();
        $("#resultado").empty(); // limpa o conteúdo da div
        $("#processamento").empty();
    });

});
function limparTudo(){
    $("#resultado").empty(); // limpa o conteúdo da div
    $("#processamento").empty();
}


