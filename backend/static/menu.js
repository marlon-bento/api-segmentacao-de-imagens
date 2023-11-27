
$(document).ready(function() {
    mostrarGray()
    // Adicione um ouvinte de evento para o link
    $("#click-gray").click(function() {
        mostrarGray();
        $("#resultado").empty(); // limpa o conteúdo da div
        $("#processamento").empty(); 
    });
    $("#click-chroma").click(function() {
        mostrarChromaKey();
        $("#resultado").empty(); // limpa o conteúdo da div
        $("#processamento").empty();
    });
    $("#click-limiarizacao").click(function() {
        mostrarLimiarizacao();
        $("#resultado").empty(); // limpa o conteúdo da div
        $("#processamento").empty();
    });
    $("#click-sobel").click(function() {
        mostrarSobel();
        $("#resultado").empty(); // limpa o conteúdo da div
        $("#processamento").empty();
    });
});


function mostrarGray() {
    $('.tom-cinza').show();
    $('.chroma-key').hide();
    $('.limiarizacao').hide();
    $('.sobel').hide();
}
function mostrarChromaKey() {
    $('.tom-cinza').hide();
    $('.chroma-key').show();
    $('.limiarizacao').hide();
    $('.sobel').hide();
}
function mostrarLimiarizacao() {
    $('.tom-cinza').hide();
    $('.chroma-key').hide();
    $('.limiarizacao').show();
    $('.sobel').hide();
}
function mostrarSobel() {
    $('.tom-cinza').hide();
    $('.chroma-key').hide();
    $('.limiarizacao').hide();
    $('.sobel').show();
}
