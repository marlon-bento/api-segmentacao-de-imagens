// Globais
var showEtapas = false;

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

function mostrarEtapas(){
    if(showEtapas){
        $('#processamento').toggleClass('d-none');
        $('#botaoMostrar').innerHTML = `Mostrar Etapas`;
        document.querySelector('#resultado').scrollIntoView({behavior: 'smooth'});
    }
    else{
        $('#processamento').toggleClass('d-none');
        $('#botaoMostrar').innerHTML = `Esconder Etapas`;
    }
        
}
