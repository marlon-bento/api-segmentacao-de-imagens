
$(document).ready(function() {
    mostrarGray()
    // Adicione um ouvinte de evento para o link
    $("#click-gray").click(function() {
        mostrarGray();
        $("#resultado").empty(); // limpa o conteúdo da div
    });
    $("#click-chroma").click(function() {
        mostrarChromaKey();
        $("#resultado").empty(); // limpa o conteúdo da div
    });
    $("#click-limiarizacao").click(function() {
        mostrarLimiarizacao();
        $("#resultado").empty(); // limpa o conteúdo da div
    });
});


function mostrarGray() {
    $('.tom-cinza').show();
    $('.chroma-key').hide();
    $('.limiarizacao').hide();
}
function mostrarChromaKey() {
    $('.tom-cinza').hide();
    $('.chroma-key').show();
    $('.limiarizacao').hide();
}
function mostrarLimiarizacao() {
    $('.tom-cinza').hide();
    $('.chroma-key').hide();
    $('.limiarizacao').show();
}
