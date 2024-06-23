//Andjela Ciric 0066/2021
document.addEventListener("DOMContentLoaded", function(){
    const form = document.getElementById('search_form');
    const input = document.getElementById('search_input');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let search = input.value;
        let searchURL=";";
        search = search.trim().toLowerCase();
        if(search==="orao krstaš" ||search ==="orao krstas" || search=="krstas" || search == "krstaš"){
            $(".OK").fadeIn()
            $(".S").fadeOut()
            $(".VD").fadeOut()
            $(".OB").fadeOut()
            searchURL="./orao_krstas.html";
        }
        else if(search==="orao belorepan" || search=="belorepan" ){
            $(".OB").fadeIn()
            $(".S").fadeOut()
            $(".VD").fadeOut()
            $(".OK").fadeOut()
            $(".hidden_p").fadeOut()
            searchURL="./orao_belorepan.html";
        }
        else if (search=="orao" || search == "Orao"){
            $(".OK").fadeIn()
            $(".S").fadeOut()
            $(".VD").fadeOut()
            $(".OB").fadeIn()
            $(".hidden_p").fadeOut()
            searchURL="./orlovi.html";
        }
        else if(search==="slavuj"){
            $(".OK").fadeOut()
            $(".S").fadeIn()
            $(".VD").fadeOut()
            $(".OB").fadeOut()
            $(".hidden_p").fadeOut()
            searchURL="./slavuji.html";
        }
        else if(search==="velika droplja" || search === "droplja"){
            $(".VD").fadeIn()
            $(".S").fadeOut()
            $(".OK").fadeOut()
            $(".OB").fadeOut()
            $(".hidden_p").fadeOut()
            searchURL="./droplje.html";
        }
        else {
            searchURL = "./pogresna_pretraga.html";
            $(".VD").fadeOut()
            $(".S").fadeOut()
            $(".OK").fadeOut()
            $(".OB").fadeOut()
            $(".hidden_p").fadeIn()
        }
    });


});

$(document).ready(function() {
    $('#inbox').click(function() {
        if ($('#inbox-section').is(':hidden')) {
            $('#inbox-section').fadeIn();
        } else {
            $('#inbox-section').fadeOut();
        }
    });
    $(document).click(function(event) {
        if (!$(event.target).closest('#inbox-section, #ikonice').length) {
            $('#inbox-section').fadeOut();
        }
    });
});

function procitanaNovost(button) {
    var novostContainer = button.parentNode; 
    novostContainer.style.display = "none"; 

    var novostiIspod = document.querySelectorAll('.container.novost:not([style="display: none;"])');

    novostiIspod.forEach(function(div) {
        div.style.transform = "translateY(-" + novostContainer.clientHeight + "px)";
    });
}

function idiNaPrijavu(){
    window.location.href = "./Prijava.html";
}

function odjaviSe(){
    window.location.href = "./index_neulogovani.html";
}