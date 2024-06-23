// Srđan Lučić 0260/2021
$(document).ready(function(){

    $(".button_delete_message").click(function(){
        let userChoice = confirm("Da li ste sigurni da želite da obrišete poruku?")
        if (userChoice){
            msgId = $(this).attr('id').split('_')[2]
            document.getElementById("delete_btn_"+msgId).innerHTML='<span class = "spinner-border spinner-border-sm"></span>X'
            deleteMessage(msgId)
        }
    })

    function deleteMessage(msgId){
        fetch('/api/obrisi_poruku/'+msgId, {

        }).then(response => {
            if(response.ok){
                return response.json()
            } else {
                console.log("Greska")
            }
        }).then(data=>{
            document.getElementById("row_"+msgId).style.display='none'
        }).catch(error => {
            console.log('Error', error)
        })
    }
})