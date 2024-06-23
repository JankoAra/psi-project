// Andjela Ciric 2021/0066

$(document).ready(function() {
    $('#inbox').click(function() {
        if ($('#inbox-section').is(':hidden')) {
            $('#inbox-section').fadeIn();
        } else {
            $('#inbox-section').fadeOut();
        }
    });
    $(document).click(function(event) {
        if (!$(event.target).closest('#inbox-section, #nav-profile').length) {
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