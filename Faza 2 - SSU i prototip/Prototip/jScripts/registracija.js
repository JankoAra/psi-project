// Autor: Srdjan Lucic 2021/0260

let prijavljeniKorisnik=null
let korisnici=[]

function inicijalizacija(){
    korisnici=JSON.parse(localStorage.getItem('korisnici'));
    if (korisnici==null) {
        korisnici=[{
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
        }];
        localStorage.setItem('korisnici',JSON.stringify(korisnici));
    } 
    prijavljeniKorisnik=JSON.parse(localStorage.getItem('prijavljeniKorisnik'));

    if (prijavljeniKorisnik==null) {
        prijavljeniKorisnik='nema';
        localStorage.setItem('prijavljeniKorisnik',JSON.stringify('nema'));
    }
    //if (prijavljeniKorisnik!='nema') document.getElementById('prijavaLink').innerHTML="<span class='nav-link'>"+prijavljeniKorisnik.korIme+"</span>"
    //else document.getElementById('prijavaLink').innerHTML='<a class="nav-link" href="Prijava.html">Prijava</a>';

    document.getElementById('registracija_button_ID').addEventListener('click', registracija);
}

function registracija(){
    let noviKorisnik={
        korIme: document.getElementById('korisnickoImeRegistracija').value,
        email: document.getElementById('emailAdresaRegistracija').value,
        lozinka: document.getElementById('lozinkaRegistracija').value,
        potvrdaLozinke: document.getElementById('potvrdaLozinkeRegistracija').value
    }
    if (noviKorisnik.korIme=='' || noviKorisnik.lozinka=='' || noviKorisnik.email=='' || noviKorisnik.potvrdaLozinke==''){
        document.getElementById('greskaRegistracija').innerHTML='Greška. Popunite sva polja.'
        return;
    } 
    else if (noviKorisnik.lozinka.length<8){
        document.getElementById('greskaRegistracija').innerHTML='Greška. Lozinka ne smije biti kraca od 8 znakova'
        return;
    } else if (noviKorisnik.lozinka != noviKorisnik.potvrdaLozinke){
        document.getElementById('greskaRegistracija').innerHTML='Greška. Lozinka i potvrda lozinke moraju biti iste.'
        return;
    } else {
        for (let i=0;i<korisnici.length;i++){
            if (korisnici[i].korIme==noviKorisnik.korIme){
                document.getElementById('greskaRegistracija').innerHTML='Greška. Korisnicko ime vec postoji.'
                return;
            }
        }
    }
    korisnici.push(noviKorisnik);
    localStorage.setItem('korisnici', JSON.stringify(korisnici));
    prijavljeniKorisnik=noviKorisnik;
    localStorage.setItem('prijavljeniKorisnik',JSON.stringify(noviKorisnik));
    document.getElementById('greskaRegistracija').innerHTML='';
    
    prelazNaPocetnu()
}

function prelazNaPocetnu(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    trenutnaPutanja+='/index.html';

    window.location.href=trenutnaPutanja
}

inicijalizacija()