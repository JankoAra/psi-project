// Autor: Srdjan Lucic 2021/0260


function inicijalizacijaPrijavaNepravilnosti(){
    document.getElementById('prijavi_button_ID').addEventListener('click',prijavi);
    document.getElementById('odustani_button_ID').addEventListener('click',odustani);

    prijavljeniKorisnik=JSON.parse(localStorage.getItem('prijavljeniKorisnik'));

    if (prijavljeniKorisnik==null) {
        prijavljeniKorisnik='nema';
        localStorage.setItem('prijavljeniKorisnik',JSON.stringify('nema'));
    }
}

function prijavi(){
    let trenutnaPutanja=window.location.pathname;
    if (trenutnaPutanja.endsWith("prijava_nepravilnosti_clanak.html")){
        if (document.getElementById("opis_prijave_nepravilnosti").value=='') {
            document.getElementById("greska_pri_prijavi").innerHTML="Greška. Opis nepravilnosti ne sme da ostane prazan.";
            return;
        } else if (document.getElementById("opis_prijave_nepravilnosti").value.length>300){
            document.getElementById("greska_pri_prijavi").innerHTML="Greška. Opis nepravilnosti ne sme da ima više od 300 znakova.";
            return;
        }
    }
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/prijava_nepravilnosti_kraj.html';

    window.location.href=trenutnaPutanja
}  

function odustani(){
    history.back();
}

inicijalizacijaPrijavaNepravilnosti()