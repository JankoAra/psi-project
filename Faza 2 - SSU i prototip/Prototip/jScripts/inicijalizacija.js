// Autor: Srdjan Lucic 2021/0260
let prijavljeniKorisnik=null;

function inicijalizacija(){
    if (document.getElementById("button_to_prijava")!=null) document.getElementById("button_to_prijava").addEventListener('click',prelazNaPrijavu)
    if (document.getElementById("button_to_registracija")!=null) document.getElementById("button_to_registracija").addEventListener('click',prelazNaRegistraciju)
    if (document.getElementById("dugme_odjava")!=null) document.getElementById("dugme_odjava").addEventListener('click', odjava)
    

    korisnici=JSON.parse(localStorage.getItem('korisnici'));
    if (korisnici==null) {
        korisnici=[
            {
                korIme: "admin123",
                email: "admin123@gmail.com",
                lozinka: "admin123",
                potvrdaLozinke: "admin123"
            },
            {
                korIme: "urednik123",
                email: "urednik123@gmail.com",
                lozinka: "urednik123",
                potvrdaLozinke: "urednik123"
            }
    ];
        localStorage.setItem('korisnici',JSON.stringify(korisnici));
    } 
    prijavljeniKorisnik=JSON.parse(localStorage.getItem('prijavljeniKorisnik'));

    if (prijavljeniKorisnik==null) {
        prijavljeniKorisnik='nema';
        localStorage.setItem('prijavljeniKorisnik',JSON.stringify('nema'));
    }

    if (document.getElementById("ulogovan_button")!=null && prijavljeniKorisnik!=null && prijavljeniKorisnik.korIme=="admin123"){
        document.getElementById("ulogovan_button").innerHTML="Ulogovani kao: admin123"
    } 

    /*if (prijavljeniKorisnik!=null && prijavljeniKorisnik.korIme=='urednik123'){
        let linkoviDetaljnije = document.querySelectorAll(".link_detaljnije")
        linkoviDetaljnije.forEach (link => {
            link.setAttribute('href', "./pregled_clanka_urednik.html")
        });
    }*/
    

    //if (prijavljeniKorisnik!='nema') document.getElementById('prijavaLink').innerHTML="<span class='nav-link'>"+prijavljeniKorisnik.korIme+"</span>"
    //else document.getElementById('prijavaLink').innerHTML='<a class="nav-link" href="Prijava.html">Prijava</a>';

    //document.getElementById('prijava_button_ID').addEventListener('click',prijava);
}

function prelazNaPrijavu(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/prijava.html';

    window.location.href=trenutnaPutanja
}

function prelazNaRegistraciju(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/registracija.html';

    window.location.href=trenutnaPutanja
}

function odjava(){
    prijavljeniKorisnik='nema';
    localStorage.setItem('prijavljeniKorisnik',JSON.stringify('nema'));

    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/index_neulogovani.html';

    window.location.href=trenutnaPutanja
}

inicijalizacija()