// Autor: Srdjan Lucic 2021/0260

let prijavljeniKorisnik=null
let korisnici=[]

function inicijalizacijaPrijava(){
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

    document.getElementById('prijava_button_ID').addEventListener('click',prijava);
}

function prijava(){
    let novaPrijava={
        korIme: document.getElementById('korisnickoImePrijava').value,
        lozinka: document.getElementById('lozinkaPrijava').value
    }

    for (let i=0;i<korisnici.length;i++){
        if (korisnici[i].korIme==novaPrijava.korIme && korisnici[i].lozinka==novaPrijava.lozinka){
            prijavljeniKorisnik=korisnici[i];
            localStorage.setItem('prijavljeniKorisnik', JSON.stringify(prijavljeniKorisnik));
            document.getElementById('korisnickoImePrijava').value=''
            document.getElementById('lozinkaPrijava').value=''
            document.getElementById('greskaPrijava').innerHTML=""
            prelazNaPocetnu()
            return;
        }
    }
    /*document.getElementById('korImePrijava').value=''
    document.getElementById('LozinkaPrijava').value=''*/
    document.getElementById('greskaPrijava').innerHTML="Pogrešno korisničko ime ili loznika."
}  

function prelazNaPocetnu(){
    let trenutnaPutanja=window.location.pathname;
    trenutnaPutanja=trenutnaPutanja.substring(0,trenutnaPutanja.lastIndexOf('/'));
    if (prijavljeniKorisnik.korIme=='admin123') trenutnaPutanja+='/index_admin.html';
    else if (prijavljeniKorisnik.korIme==='urednik123')trenutnaPutanja+='/index_urednik.html'
    else trenutnaPutanja+='/index.html';

    window.location.href=trenutnaPutanja
}

inicijalizacijaPrijava()