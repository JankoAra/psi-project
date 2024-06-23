// Janko Arandjelovic 2021/0328
// Anđela Ćirić 2021/0066


// Promenljive ubacene iz Djanga: userAuthenticated, username, articleID, userType, 
// csrfToken, articleAuthorUsername, startAvgGrade, userGrade
$(document).ready(function () {

    //ucitavanje galerije i diskusija po ucitavanju clanka
    getGalleryImages();
    getDiscussions();
    getButtonTrackChanges();

    //konverzija parametara prosledjenih iz Djanga u odgovarajuce tipove
    userAuthenticated = userAuthenticated === "True" ? true : false;
    startAvgGrade = startAvgGrade.replace(/,/g, '.');
    startAvgGrade = parseFloat(startAvgGrade);
    userGrade = parseInt(userGrade);

    //postavljanje prosecne ocene i izabrane ocene ulogovanog korisnika(ako postoji)
    $("#prosecna-ocena-value").text(startAvgGrade.toFixed(2));


    //povremeno osvezavanje sadrzaja stranice
    const refreshIntervalMinutes = 5;

    setInterval(() => {
        getGalleryImages();
        getDiscussions();
        getAvgGrade();
        getButtonTrackChanges()
    }, refreshIntervalMinutes * 60 * 1000);


    /* IZMENA SADRZAJA CLANKA I TABELE INFORMACIJA(za admine i urednika-autora) */

    //klik na dugme za promenu slike u tabeli informacija, prikazuje se forma za izbor nove slike
    $("#show-change-table-image-btn").on("click", function () {
        $("#tabela_slika_file").show();
        $("#cancel-change-table-image-btn").show();
        $("#change-table-image-form").show();
        $(this).hide();
        $("#show-delete-table-image-btn").hide();
    });

    //klik na dugme za odustajanje od promene slike u tabeli informacija, forma za izbor nove slike se sakriva
    $("#cancel-change-table-image-btn").on("click", function () {
        $("#tabela_slika_file").hide();
        $("#change-table-image-form").hide();
        $("#cancel-change-table-image-btn").hide();
        $("#show-change-table-image-btn").show();
        $("#show-delete-table-image-btn").show();
        $("#tabela_slika_file").val("");
    });

    $("#show-delete-table-image-btn").on("click", function () {
        openDeleteConfirmationModal("tableImage", articleID);
    });


    //klik na dugme za promenu informacija u tabeli, prikazuje se forma za izbor novih informacija,
    //stare vrednosti su pocetne vrednosti forme
    $("#show-change-article-table-form-btn").on("click", function () {
        let tableFields = $(".tabela_info");
        tableFields.each(function () {
            let val = $(this).text();
            let inputField = $(this).next();
            $(inputField).val(val);
            if ($(inputField).attr("type") === "number") {
                val = val.replace(/,/g, ".");   //brojevi se lokalizovano pisu sa zarezom, problem pri parsiranju
                $(inputField).val(parseFloat(val));
            }
            $(this).hide();
            $(inputField).show();
        });
        $(this).hide();
        $("#cancel-change-article-table-form-btn").show();
        $("#submit-change-article-table-form-btn").show();
        $("#tabela_vrsta_form_change").focus();
    });

    //klik na dugme za odustajanje od promene informacija u tabeli, forma za izbor novih informacija se sakriva
    $("#cancel-change-article-table-form-btn").on("click", function () {
        let tableFields = $(".tabela_info");
        tableFields.each(function () {
            $(this).show();
            $(this).next().hide();
        });
        $(this).hide();
        $("#show-change-article-table-form-btn").show();
        $("#submit-change-article-table-form-btn").hide();
    });


    //klik na dugme za prihvatanje izmena informacija u tabeli
    $("#submit-change-article-table-form-btn").on("click", function () {
        changeTableInformation();
    });

    //klik na dugme za prikaz forme za prikaz teksta clanka, pocetni tekst forme je trenutni teskt clanka
    $("#show-change-article-text-form-btn").on("click", function () {
        $("#change-article-text").show();
        $(this).hide();
        $("article").hide();
        $("#new-text").val($("article p").text());
    });

    //klik na dugme za odustajanje od promene teksta
    $("#cancel-change-article-text-btn").on("click", function () {
        $("#change-article-text").hide();
        $("#show-change-article-text-form-btn").show();
        $("article").show();
    });

    //klik na dugme za prihvatanje novog teksta
    $("#submit-change-article-text-btn").on("click", function () {
        changeArticleText();
        $("#change-article-text").hide();
        $("#show-change-article-text-form-btn").show();
        $("article").show();
    });


    /* PREGLED SADRZAJA CLANKA */

    $("#track_changes_button").on("click", function () {
        trackChanges();
    });

    $("#dont_track_changes_button").on("click", function () {
        dontTrackChangesAnymore()
    })

    $("#report_error_on_article").on("click", function () {
        reportErrorOnArticle();
    });

    /* RAD SA DISKUSIJAMA */

    //dugmici za pravljenje diskusije
    $("#open-new-discussion-btn").click(showNewDiscussionForm);
    $("#cancel-new-discussion-btn").click(hideNewDiscussionForm);
    $("#submit-new-discussion-btn").click(submitDiscussion);

    //pri prelasku na neki drugi tab, ukoliko je forma za kreiranje diskusije ili komentara otvorena, sakriva se
    $("#myTabs li a").click(function (e) {
        if (this.id !== "tab3") {
            hideNewDiscussionForm();
            closeOpenCommentForms();
        }
    });

    function closeOpenCommentForms() {
        $(".forma_komentar").hide();
        $(".new-comment-button").show();
    }

    //prikazuje praznu formu za zapocinjanje nove diskusije
    function showNewDiscussionForm() {
        $("#naslov_diskusije").val("");
        $("#tekst_diskusije").val("");
        $("#nova_diskusija").show();
        $("#open-new-discussion-btn").hide();
        closeOpenCommentForms();
    }

    //sakriva formu za zapocinjanje nove diskusije
    function hideNewDiscussionForm() {
        $("#nova_diskusija").hide();
        $("#open-new-discussion-btn").show();
    }

    // Dodavanje osluskivaca na dugmice koji su dinamicki kreirani u okviru komentara
    $(document).on('click', '.delete-comment-link', function (event) {
        event.preventDefault();
        let commentId = $(this).data('id');
        openDeleteConfirmationModal('comment', commentId);
    });

    $(document).on('click', '.report-comment-link', function (event) {
        event.preventDefault();
        let commentId = $(this).data('id');
        reportIrregularityComment(commentId);
    });

    // Dodavanje osluskivaca na dugmice koji su dinamicki kreirani u okviru diskusije
    $(document).on('click', '.delete-discussion-link', function (event) {
        event.preventDefault();
        let discussionId = $(this).data('id');
        openDeleteConfirmationModal('discussion', discussionId);
    });

    $(document).on('click', '.report-discussion-link', function (event) {
        event.preventDefault();
        let discussionId = $(this).data('id');
        reportIrregularityDiscussion(discussionId);
    });


    $(document).on('click', '.new-comment-button', function () {
        closeOpenCommentForms();
        hideNewDiscussionForm();
        let discussionId = $(this).closest('.post').data('id');
        let newCommentDiv = $(this).siblings('.forma_komentar');
        $(this).hide();
        newCommentDiv.show();
        newCommentDiv.find('textarea').val('').focus();
    });

    $(document).on('click', '.submit-comment-btn', function () {
        let newCommentDiv = $(this).closest('.forma_komentar');
        let discussionId = newCommentDiv.data('discussion-id');
        let commentText = newCommentDiv.find('textarea').val();
        if (commentText === '') {
            $(".new_comment_error").text("Komentar ne sme da bude prazan");
            return;
        } else {
            $(".new_comment_error").text("");
        }
        submitComment(discussionId, commentText);
        newCommentDiv.hide();
        newCommentDiv.siblings('.new-comment-button').show();
    });

    $(document).on('click', '.cancel-comment-btn', function () {
        let newCommentDiv = $(this).closest('.forma_komentar');
        newCommentDiv.hide();
        newCommentDiv.siblings('.new-comment-button').show();
    });


    /* OCENJIVANJE */

    buildRatingDiv();
    function buildRatingDiv() {
        if (!userAuthenticated) return;
        let avgGrade = startAvgGrade;
        let usersGrade = userGrade;
        let ratingDiv = $("#rating-div");
        for (let i = 1; i <= 10; i++) {
            let spanStar = $("<span></span>");
            spanStar.addClass("fa fa-star");
            if (i <= usersGrade) {
                spanStar.addClass("checked-star");
            }
            // if (i == usersGrade) {
            //     spanStar.addClass("user-grade-star");
            // }
            spanStar.data("value", i);
            spanStar.css("cursor", "pointer");
            spanStar.on("click", function () {
                let value = $(this).data("value");
                // ratingDiv.find("span.fa-star").removeClass("user-grade-star");
                // $(this).addClass("user-grade-star");
                if (articleAuthorUsername === username) {
                    alert("Ne možete da ocenite svoj članak!");
                } else {
                    alterGrade(value);
                    usersGrade = value;
                }
            });
            spanStar.on("mouseenter", function () {
                let value = $(this).data("value");
                ratingDiv.find("span.fa-star").each(function (index) {
                    if (index < value) {
                        $(this).addClass("checked-star");
                    } else {
                        $(this).removeClass("checked-star");
                    }
                });
                chosenGradeSpan.text(value + "/10");
            });
            spanStar.on("mouseleave", function () {
                ratingDiv.find("span.fa-star").each(function (index) {
                    if (index < usersGrade) {
                        $(this).addClass("checked-star");
                    } else {
                        $(this).removeClass("checked-star");
                    }
                });
                chosenGradeSpan.text(usersGrade + "/10");
            });
            ratingDiv.append(spanStar);
        }
        ratingDiv.append($(`<span style="font-size: 20px; margin-left: 10px;">Vaša ocena: </span>`));
        var chosenGradeSpan = $(`<span></span>`);
        chosenGradeSpan.text(usersGrade + "/10");
        chosenGradeSpan.css("font-size", "20px");
        chosenGradeSpan.css("margin-left", "10px");
        ratingDiv.append(chosenGradeSpan);
        ratingDiv.addClass("mb-3");
    }

    /* MODALI */

    //prikaz modala za potvrdu brisanja sa dinamickim sadrzajem, u zavisnosti od kliknutog dugmeta
    function openDeleteConfirmationModal(type, id) {
        let title = "";
        let bodyText = "";
        let confirmButtonText = "";
        let confirmAction;

        switch (type) {
            case 'discussion':
                title = "Potvrda brisanja diskusije";
                bodyText = "Da li ste sigurni da želite da obrišete ovu diskusiju? Obrisaćete i sve komentare vezane za ovu diskusiju. Ova akcija je nepovratna!";
                confirmButtonText = "Obriši";
                confirmAction = function () {
                    deleteDiscussion(id);
                };
                break;
            case 'comment':
                title = "Potvrda brisanja komentara";
                bodyText = "Da li ste sigurni da želite da obrišete ovaj komentar? Ova akcija je nepovratna!";
                confirmButtonText = "Obriši";
                confirmAction = function () {
                    deleteComment(id);
                };
                break;
            case 'image':
                title = "Potvrda brisanja slike iz galerije";
                bodyText = "Da li ste sigurni da želite da obrišete ovu sliku iz galerije? Ova akcija je nepovratna!";
                confirmButtonText = "Obriši";
                confirmAction = function () {
                    deleteImageInGallery(id);
                };
                break;
            case 'tableImage':
                title = "Potvrda brisanja slike iz tabele informacija";
                bodyText = "Da li ste sigurni da želite da obrišete ovu sliku iz tabele informacija? Ova akcija je nepovratna!";
                confirmButtonText = "Obriši";
                confirmAction = function () {
                    deleteTableImage(id);
                };
                break;
            default:
                console.error('Unknown type for deletion modal');
                return;
        }

        $('#confirmDeleteModalLabel').text(title);
        $('#confirmDeleteModalBody').text(bodyText);
        $('#confirmDeleteButton').text(confirmButtonText).off('click').on('click', function () {
            $('#confirmDeleteModal').modal('hide');
            confirmAction();
        });

        $('#confirmDeleteModal').modal('show');
    }

    //modal za fullscreen prikaz slike
    function openImageModal(imageSrc) {
        $('#modal-image').attr('src', imageSrc);
        $('#imageModal').modal('show');

    }

    $(document).on('click', function (e) {
        if ($('#imageModal').hasClass('show')) {
            $('#imageModal').modal('hide');
        }
    });

    //prikaz dodatnih informacija o slici
    function openImageInfoModal(image) {
        let info = $(`<div class="text-center d-flex flex-column align-items-center">
            <p>Autor: ${image.username_autora}</p>
            <p>Datum postavljanja: ${image.datum_vreme}</p>
            ${userType === 'A' || userType === 'U' ? `<p>ID slike: ${image.id_fotografije}</p>` : ""}
        </div>`);

        $('#imageInfoModal .modal-body').html(info);
        $('#imageInfoModal').modal('show');
    }

    /* API POZIVI */

    //dohvata podatke iz forme za promenu tabele informacija i salje API zahtev za izmenu
    function changeTableInformation() {
        let vrsta = $("#tabela_vrsta_form_change").val().trim();
        let rod = $("#tabela_rod_form_change").val().trim();
        let porodica = $("#tabela_porodica_form_change").val().trim();
        let red = $("#tabela_red_form_change").val().trim();
        let klasa = $("#tabela_klasa_form_change").val().trim();
        let tip = $("#tabela_tip_form_change").val().trim();
        let carstvo = $("#tabela_carstvo_form_change").val().trim();
        let tezina = $("#tabela_tezina_form_change").val().trim();
        if (tezina === "") {
            tezina = "0";
            $("#tabela_tezina_form_change").val("0.00");
        }
        let velicina = $("#tabela_velicina_form_change").val().trim();
        if (velicina === "") {
            veličina = "0";
            $("#tabela_velicina_form_change").val("0.00");
        }
        let status = $("#tabela_status_form_change").val().trim();
        fetch('/api/izmena_tabele/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article_id: articleID,
                vrsta: vrsta,
                rod: rod,
                porodica: porodica,
                red: red,
                klasa: klasa,
                tip: tip,
                carstvo: carstvo,
                tezina: tezina,
                velicina: velicina,
                status: status
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno, nove vrednosti se upisuju u polja tabele informacija
                let tableFields = $(".tabela_info");
                tableFields.each(function () {
                    //console.log($(this).next().val().trim());
                    $(this).text($(this).next().val().trim());
                    $(this).show();
                    $(this).next().hide();
                });
                $("#ime_vrste_tabela").text(vrsta);
                $("article h2").text(vrsta);
            } else {
                //ako je neuspesno, tabela ostaje nepromenjena
                console.log(data.error);
            }
            $("#cancel-change-article-table-form-btn").hide();
            $("#show-change-article-table-form-btn").show();
            $("#submit-change-article-table-form-btn").hide();
        })
    }

    //dohvata podatke iz forme za promenu teksta i salje API zahtev za izmenu
    function changeArticleText() {
        let newText = $("#new-text").val();
        fetch('/api/izmena_teksta_clanka/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article_id: articleID,
                new_text: newText
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno, tekst clanka se azurira
                $("article p").text(newText);
            } else {
                //ako je neuspesno, tekst clanka ostaje nepromenjen
                console.log(data.error);
            }
        })
    }

    function deleteTableImage(articleID){
        fetch('/api/obrisi_sliku_u_tabeli/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article_id: articleID
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno, slika se uklanja iz baze
                window.location.reload();
            } else {
                //ako je neuspesno, slika ostaje u bazi
                console.log(data.error);
            }
        })
    }

    //prima ocenu koju je korisnik izabrao i salje API zahtev za dodavanje ocene u bazu
    let alterGradeWorking = false;
    function alterGrade(grade) {
        if (alterGradeWorking) return;
        alterGradeWorking = true;
        fetch('/api/izmena_ocena/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article_id: articleID,
                grade: grade
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno, ocena se azurira; prikaz selektovane ocene se azurira
                let avgRating = parseFloat(data.avg_rating);

                userGrade = grade;

                startAvgGrade = avgRating;
                $("#rating-div").find("span.fa-star").each(function (index) {
                    if (index < userGrade) {
                        $(this).addClass("checked-star");
                    } else {
                        $(this).removeClass("checked-star");
                    }
                });
                $("#prosecna-ocena-value").text(avgRating.toFixed(2));
            } else {
                //ako je neuspesno, ocena ostaje nepromenjena
                console.log(data.error);
            }
            alterGradeWorking = false;
        })
    }

    //dohvata prosecnu ocenu i prikazuje je html elementu
    function getAvgGrade() {
        fetch('/api/prosecna_ocena/' + articleID).then(response => response.json()).then(data => {
            if (data.success === true) {
                let avgRating = parseFloat(data.avg_rating);
                $("#prosecna-ocena-value").text(avgRating.toFixed(2));
            } else {
                console.log(data.error);
                $("#prosecna-ocena-value").text("Greska");
            }
        })
    }


    //dohvata sadrzaj iz forme za novu diskusiju i salje API zahtev za dodavanje nove diskusije
    function submitDiscussion() {
        let discussionTitle = $("#naslov_diskusije").val();
        let discussionContent = $("#tekst_diskusije").val();
        if (discussionTitle === "") {
            $("#naslov_diskusije_greska").text("Naslov diskusije je obavezan");
        } else {
            $("#naslov_diskusije_greska").text("");
        }
        if (discussionContent === "") {
            $("#tekst_diskusije_greska").text("Tekst diskusije je obavezan");
        } else {
            $("#tekst_diskusije_greska").text("");
        }
        if (discussionTitle === "" || discussionContent === "") {
            return;
        }
        fetch(`/api/napravi_diskusiju/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                discussion_title: discussionTitle,
                discussion_content: discussionContent,
                article_id: articleID
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success === true) {
                    //ako je uspesno, ucitavaju se sve diskusije ispocetka
                    getDiscussions();
                    hideNewDiscussionForm();
                } else {
                    //ako je neuspesno, nema promene
                    console.log(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                hideNewDiscussionForm();
            });

    }

    //dohvata sve komentare i diskusije iz baze i prikazuje ih
    function getDiscussions() {
        fetch(`/api/dohvati_diskusije/${articleID}`).then(response => response.json()).then(data => {
            const discussionContainer = $('#discussions_container');
            discussionContainer.empty();
            data.forEach(discussion => {
                const discussionElement = createDiscussionElement(discussion);
                discussionContainer.append(discussionElement);
            });
        });
    }

    //kreira HTML string koji predstavlja prosledjenu diskusiju, osluskivaci se dodaju pri ucitavanju stranice
    function createDiscussionElement(discussion) {
        let deleteDiscussionLink = "";
        let reportLink = "";

        if (userAuthenticated && (userType === 'A' || userType === 'U')) {
            deleteDiscussionLink =
                `<a class='dropdown-item delete-discussion-link' href='#' data-id='${discussion.id_diskusije}'>
                    Obriši diskusiju
                </a>`;
        }

        if (userAuthenticated) {
            reportLink =
                `<a class='dropdown-item report-discussion-link' href='#' data-id='${discussion.id_diskusije}'>
                    Prijavi diskusiju
                </a>`;
        }

        let commentsHtml = "";
        discussion.komentari.forEach(comment => {
            commentsHtml += createCommentElement(comment);
        });

        let dropdownMenu = "";
        if (userAuthenticated) {
            dropdownMenu = `
                <div class="dropdown position-absolute" style="top: 10px; right: 10px;">
                    <button class="btn btn-sm dropdown-toggle" type="button" id="dropdownMenuButton${discussion.id_diskusije}" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-ellipsis-h"></i>
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton${discussion.id_diskusije}">
                        ${userAuthenticated && userType !== 'A' ? reportLink : ""}
                        ${userAuthenticated && (userType === 'A' || userType === 'U') ? deleteDiscussionLink : ""}
                    </ul>
                </div>`;
        }

        let discussionDiv = `
            <div class="post row g-2 position-relative my-2">
                <div class="col-4 col-md-2 text-center align-self-center border-end border-dark border-2">
                    <p class="discussion-autor-username">Autor:<br>${discussion.autorDiskusije}</p>
                    <hr>
                    <p class="discussion-date">Datum objave:<br>${discussion.datumVreme}</p>
                </div>
                <div class="col-8 col-md-10 px-2">
                    <h3 class="discussion-title">${discussion.naslov}</h3>
                    <p class="keep-whitespace">${discussion.sadrzaj}</p>
                    ${dropdownMenu}
                </div>
                <hr>
                <div class="col-12 col-md-10 offset-md-2">
                    <h6>Komentari</h6>
                    ${userAuthenticated ? `<button class="new-comment-button btn btn-success my-1">+ Dodaj komentar</button>` : ""}
                    <div class="forma_komentar" data-discussion-id="${discussion.id_diskusije}" style="display: none;">
                        <textarea rows="5" class="w-100" placeholder="Tekst komentara"></textarea><span class="new_comment_error" style="color: red;"></span><br>
                        <button class="submit-comment-btn btn btn-success">Potvrdi</button>
                        <button class="cancel-comment-btn btn btn-secondary">Odustani</button>
                    </div>
                    ${commentsHtml}
                </div>
            </div>`;

        return discussionDiv;
    }

    //kreira HTML string koji predstavlja prosledjeni komentar, osluskivaci se dodaju pri ucitavanju stranice
    function createCommentElement(comment) {
        let deleteCommentLink = "";
        let reportLink = "";

        if (userAuthenticated && (userType === 'A' || userType === 'U')) {
            deleteCommentLink =
                `<a class='dropdown-item delete-comment-link' href='#' data-id='${comment.id_komentara}'>
                Obriši komentar
            </a>`;
        }

        if (userAuthenticated) {
            reportLink =
                `<a class='dropdown-item report-comment-link' href='#' data-id='${comment.id_komentara}'>
                Prijavi komentar
            </a>`;
        }

        let dropdownMenu = "";
        if (userAuthenticated) {
            dropdownMenu = `
            <div class="dropdown position-absolute" style="top: 10px; right: 10px;">
                <button class="btn btn-sm dropdown-toggle" type="button" id="dropdownMenuButtonComment${comment.id_komentara}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButtonComment${comment.id_komentara}">
                    ${userAuthenticated && userType !== 'A' ? reportLink : ""}
                    ${userAuthenticated && (userType === 'A' || userType === 'U') ? deleteCommentLink : ""}
                </ul>
            </div>`;
        }

        let commentDiv =
            `<div class="comment position-relative">
            <p>Autor: ${comment.autorKomentara} <br>Datum: ${comment.datumVreme}</p>
            <p class="keep-whitespace">${comment.sadrzaj}</p>
            ${dropdownMenu}
        </div>`;

        return commentDiv;
    }


    //API poziv za brisanje diskusije sa datim ID
    function deleteDiscussion(discussionID) {
        fetch(`/api/obrisi_diskusiju/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                discussion_id: discussionID
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno obrisana diskusija, prikazuju se preostale diskusije
                getDiscussions();
            } else {
                console.log(data.error);
            }
        })
    }

    //API poziv za dodavanje novog komentara
    function submitComment(discussionID, commentText) {
        fetch(`/api/dodaj_komentar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                discussion_id: discussionID,
                comment_content: commentText
            })
        }).then(response => response.json()).then(data => {
            if (data.success === true) {
                //ako je uspesno dodat novi komentar, prikazuju se sve diskusije sa komentarima
                getDiscussions();
            } else {
                console.log(data.error);
            }
        })
    }

    //API poziv za dohvatanje slika u galeriji nekog clanka, slike se ugradjuju u HTML
    function getGalleryImages() {
        fetch(`/api/dohvati_slike_u_galeriji/${articleID}`)
            .then(response => response.json())
            .then(data => {
                const imageContainer = document.querySelector('.image-container');
                imageContainer.innerHTML = '';
                data.forEach(image => {
                    const imageItem = document.createElement('div');
                    imageItem.classList.add('image-item', 'col');
                    const img = document.createElement('img');
                    img.src = `data:image/png;base64,${image.sadrzaj_slike}`;
                    img.classList.add('img-fluid');
                    img.alt = 'Slika u galeriji';
                    if (userAuthenticated && (userType === 'A' || userType === 'U')) {
                        img.title = "Slika ID: " + image.id_fotografije;
                    }
                    img.addEventListener('click', function () {
                        openImageModal(img.src);
                    });
                    imageItem.appendChild(img);

                    if (userAuthenticated) {
                        // Dropdown meni sa dodatnim opcijama
                        const dropdown = document.createElement('div');
                        dropdown.classList.add('dropdown', 'position-absolute');
                        dropdown.style.top = '10px';
                        dropdown.style.right = '10px';

                        const dropdownToggle = document.createElement('button');
                        dropdownToggle.classList.add('btn', 'btn-sm', 'text-white', 'dropdown-toggle', 'm-1');
                        dropdownToggle.setAttribute('data-bs-toggle', 'dropdown');
                        dropdownToggle.innerHTML = '<i class="fas fa-ellipsis-h"></i>';
                        dropdown.appendChild(dropdownToggle);

                        const dropdownMenu = document.createElement('div');
                        dropdownMenu.classList.add('dropdown-menu');
                        if (userAuthenticated && userType !== 'A') {
                            const reportItem = document.createElement('button');
                            reportItem.classList.add('dropdown-item');
                            reportItem.textContent = 'Prijavi nepravilnost';
                            reportItem.addEventListener('click', function () {
                                reportIrregularityPhotoraph(image.id_fotografije);
                            });
                            dropdownMenu.appendChild(reportItem);
                        }

                        if (userAuthenticated &&
                            (userType === 'A' || userType === 'U' ||
                                (userType === 'R' && username === image.username_autora))) {
                            const deleteItem = document.createElement('button');
                            deleteItem.classList.add('dropdown-item');
                            deleteItem.textContent = 'Obriši sliku';
                            deleteItem.addEventListener('click', function () {
                                openDeleteConfirmationModal('image', image.id_fotografije);
                            });
                            dropdownMenu.appendChild(deleteItem);
                        }

                        let infoItem = document.createElement('button');
                        infoItem.classList.add('dropdown-item');
                        infoItem.textContent = 'Dodatne informacije';
                        infoItem.addEventListener('click', function () {
                            openImageInfoModal(image);
                        });
                        dropdownMenu.appendChild(infoItem);

                        dropdown.appendChild(dropdownMenu);
                        imageItem.appendChild(dropdown);
                    }
                    imageContainer.appendChild(imageItem);
                });
            })
            .catch(error => console.error('Error fetching images:', error));
    }



    //API poziv za brisanje slike iz galerije
    function deleteImageInGallery(imageId) {
        fetch(`/api/obrisi_sliku_u_galeriji/${imageId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                username: username,
                userType: userType,
                image_id: imageId
            })
        }).then(response => {
            if (response.ok) {
                console.log('Image deleted successfully');
                getGalleryImages();
            } else {
                console.error('Error deleting image:', response.statusText);
            }
        })
    }

    //API poziv za brisanje komentara
    function deleteComment(commentID) {
        fetch(`/api/obrisi_komentar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                comment_id: commentID
            })
        }).then(response => {
            if (response.ok) {
                console.log('Comment deleted successfully');
                getDiscussions();
            } else {
                console.error('Error deleting comment:', response.statusText);
            }
        })
    }

    //API poziv za prijavljivanje nepravilnosti slike
    //Šalje se fetch zahtev i na osnovu pozitivnog response prelazi se na stranicu za prijavu nepravilnosti slike
    function reportIrregularityPhotoraph(imageId) {
        fetch('prijavi_nepravilnost_slike_prelaz/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                imageId: imageId
            })
        }).then(response => {
            if (response.ok) {
                console.log("Moved to page irregularity of photograph")
                //window.location.href = `/prijavi_nepravilnost_slike/?imageId=${imageId}`;
                window.location.href = '/prijavi_nepravilnost_slike/' + imageId;
            } else {
                console.error('Error response irregularity photograph', response.statusText);
            }
        }).catch(error => {
            console.error('Error', error);
        });
    }

    //API poziv za prijavljivanje nepravilnosti komentara
    //Šalje se fetch zahtev i na osnovu pozitivnog response prelazi se na stranicu za prijavu nepravilnosti odgovarajućeg komentara
    function reportIrregularityComment(idComm) {
        fetch('prijavi_nepravilnost_komentara_prelaz/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                idComm: idComm
            })
        }).then(response => {
            if (response.ok) {
                console.log("Moved to page irregularity of comment")
                window.location.href = '/prijavi_nepravilnost_komentara/' + idComm;
            } else {
                console.error('Error response irregularity comment', response.statusText);
            }
        }).catch(error => {
            console.error('Error', error);
        });
    }

    //API poziv za prijavljivanje nepravilnosti diskusije
    //Šalje se fetch zahtev i na osnovu pozitivnog response prelazi se na stranicu za prijavu nepravilnosti odgovarajuće diskusije
    function reportIrregularityDiscussion(idDis) {
        fetch('prijavi_nepravilnost_diskusije_prelaz/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                idDiscuss: idDis
            })
        }).then(response => {
            if (response.ok) {
                console.log("Moved to page irregularity of discussion")
                window.location.href = '/prijavi_nepravilnost_diskusije/' + idDis;
            } else {
                console.error('Error response irregularity discussion', response.statusText);
            }
        }).catch(error => {
            console.error('Error', error);
        });
    }

    //API poziv koji u zavisnoti od toga da li se korisnik prijavio da prati izmene prikazuje dugme za prijavu ili za odjavu
    //Šalje se fetch zahtev i na osnovu response određuje koju opciju treba prikazati trenutno ulogovanom korisniku u zavinosti od toga da li se već prijavio na praćenje obaveštenja ili ne
    function getButtonTrackChanges() {
        let button_track_changes = document.getElementById("track_changes_button")
        // Dodato dugme za odjavu od pracenja obavjestenja
        let button_dont_track_changes = document.getElementById('dont_track_changes_button')
        if (button_track_changes != null) {
            let show = 0;
            fetch(`/api/dohvati_prijavljen_na_obavestenja/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    article: articleID
                })
            }).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    console.log('Error checking if already exists');
                }
            }).then(data => {
                if (data.success) {
                    console.log("show");
                    // button_track_changes.style.display = "block";
                    // button_dont_track_changes.style.display = "none";
                    $(button_track_changes).show();
                    $(button_dont_track_changes).hide();
                } else {
                    console.log("dont show");
                    // button_track_changes.style.display = "none";
                    // button_dont_track_changes.style.display = "block";
                    $(button_dont_track_changes).show();
                    $(button_track_changes).hide();
                }
            }).catch(error => {
                console.error('Fetch error:', error);
            });
        }
    }

    //API poziv koji započinje prijavljivanje korisnika za praćenje izmena na članku
    //Šalje se fetch zahtev i na osnovu pozitivnog response prelazi se na stranicu za prijavu na praćenje obaveštenja sa odgovarajućom formom

    function trackChanges() {
        fetch('prijavi_se_na_pracenje_obavestenja_prelaz/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article: articleID
            })
        }).then(response => {
            if (response.ok) {
                console.log("Moved to page want to track changes")
                window.location.href = '/prijavi_se_na_pracenje_obavestenja/' + articleID;
            } else {
                console.error('Error response want to track changes', response.statusText);
            }
        }).catch(error => {
            console.error('Error', error);
        });
    };

    function dontTrackChangesAnymore() {
        button_track_changes = document.getElementById('track_changes_button')
        button_dont_track_changes = document.getElementById('dont_track_changes_button')
        fetch('/api/odjavi_se_sa_pracenja_obavjestenja/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article: articleID
            })
        }).then(response => {
            if (!response.ok) {
                console.error('Error response stop tracking changes', response.statusText);
            } else {
                // button_track_changes.style.display = "block";
                // button_dont_track_changes.style.display = "none";
                $(button_track_changes).show();
                $(button_dont_track_changes).hide();
            }
        }).catch(error => {
            console.error('Error', error);
        });
    };

    //API poziv za prijavu nepravilnosti članka
    //Šalje se fetch zahtev i na osnovu pozitivnog response prelazi se na stranicu za prijavu nepravilnosti članka
    function reportErrorOnArticle() {
        fetch('prijavi_nepravilnost_clanka_prelaz/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                article: articleID
            })
        }).then(response => {
            if (response.ok) {
                console.log("Moved to page report error on article")
                window.location.href = '/prijavi_nepravilnost_clanka/' + articleID;
            } else {
                console.error('Error response want report error on article', response.statusText);
            }
        }).catch(error => {
            console.error('Error', error);
        });
    };
});



