// Autor: Srdjan Lucic 2021/0260

function inicijalizacija(){
    inicijalizacijaDugmeClanak()
    inicijalizacijaDugmeDiskusijaKomentar()
    inicijalizacijaDugmeFotografija()
}

function inicijalizacijaDugmeClanak(){
    document.getElementById('prijava_clanka_button').addEventListener('click', formaPrijavaClanka)
}

function inicijalizacijaDugmeFotografija(){
    dugmadFotografija = document.querySelectorAll('.prijava_galerija_button');

        dugmadFotografija.forEach(button => {
            button.addEventListener('click', formaPrijavaFotografije);
        });
}

function inicijalizacijaDugmeDiskusijaKomentar(){
    dugmadDiskusija = document.querySelectorAll('.prijava_diskusije_button');

    dugmadDiskusija.forEach(button => {
        button.addEventListener('click', formaPrijavaDiskusijeKomentara);
    });
}

function formaPrijavaClanka(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/prijava_nepravilnosti_clanak.html';

    window.location.href=trenutnaPutanja
}

function formaPrijavaFotografije(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/prijava_nepravilnosti_galerija.html';

    window.location.href=trenutnaPutanja
}

function formaPrijavaDiskusijeKomentara(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/prijava_nepravilnosti_komentar.html';

    window.location.href=trenutnaPutanja
}

setInterval(inicijalizacija,500);

//inicijalizacija()