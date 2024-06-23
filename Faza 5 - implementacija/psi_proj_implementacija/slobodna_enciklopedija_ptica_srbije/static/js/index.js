// Srđan Lučić 0260/2021
$(document).ready(function(){

    const months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'sep', 'okt', 'nov', 'dec']

    function load_more(){
        containerForArticles = document.getElementById('container-article-brief')

        document.getElementById('load_more_button').innerHTML=
            '<span class = "spinner-border spinner-border-sm"></span> Učitavanje...'

        fetch('/api/index_ucitaj_vise/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                number_of_articles: numberOfLoadedArticles
            })
        }).then(response => {
            if (response.ok){
                return response.json()
            } else {
                console.log("Greska u ucitavanju vise")
            }
        }).then(data => {
            numberOfLoadedArticles = parseInt(data.number_of_loaded_articles)
            if (numberOfLoadedArticles == totalArticles) {
                document.getElementById('load_more_button').style.display='none'
            } else {
                document.getElementById('load_more_button').innerHTML = "Učitajte više..."
            }
            data.articles.forEach(article => {
                reformatDate(article)
                reformatDecimalNumbers(article)
                console.log(article.creationDate)
                newArticleView = render_article(article)
                document.getElementById('container-article-brief').innerHTML =
                    document.getElementById('container-article-brief').innerHTML + newArticleView
            })
        }).catch(error => {
            console.error("Greska")
        })
    }

    function render_article(article){
        articleTemplate = '<div class="row bird-container bird-info">\n' +
            '                    <div class="col-lg-4 col-6 bird-image d-flex flex-column justify-content-center">\n' +
            '                        <img src="'+article.image+'" alt="'+ article.species +'">\n' +
            '                    </div>\n' +
            '\n' +
            '                    <div class="col-lg-8 col-6 bird-details">\n' +
            '                        <h3 class="bird-naslov text-right">'+article.species+'</h3>\n' +
            '                        <h6 class="bird-naslov text-right">'+article.creationDate+'</h6>\n' +
            '                    <h6 class="bird-naslov text-right">Prosečna ocena: <kbd>'+ article.avg_pts +'</kbd></h6>\n' +
            '                        <table class="bird-table float-right">\n' +
            '                            <tr>\n' +
            '                                <th class="bird-th">Vrsta</th>\n' +
            '                                <td class="bird-td">'+ article.species +'</td>\n' +
            '                            </tr>\n' +
            '                            <tr>\n' +
            '                                <th class="bird-th">Porodica</th>\n' +
            '                                <td class="bird-td">'+ article.family +'</td>\n' +
            '                            </tr>\n' +
            '                            <tr>\n' +
            '                                <th class="bird-th">Težina</th>\n' +
            '                                <td class="bird-td">'+ article.weight +'</td>\n' +
            '                            </tr>\n' +
            '                            <tr>\n' +
            '                                <th class="bird-th">Veličina</th>\n' +
            '                                <td class="bird-td">'+ article.size +'</td>\n' +
            '                            </tr>\n' +
            '                            <tr>\n' +
            '                                <th class="bird-th">Status ugroženosti</th>\n' +
            '                                <td class="bird-td"><div class="w-35 bg-warning">'+ article.conservation +'</div></td>\n' +
            '                            </tr>\n' +
            '                        </table>\n' +
            '\n' +
            '                        <p class="bird-p"> <!--text-right-->\n' +
            '                            '+ article.text +'\n' +
            '                            <a class="link-dark link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" href="'+ article.routeToArticle+'">Detaljnije</a>\n' +
            '                        </p>\n' +
            '                    </div>\n' +
            '            <!--/div-->\n' +
            '    </div>'
        return articleTemplate
    }

    function reformatDate(article){
        let newDate = new Date(article.creationDate)
        article.creationDate = newDate.toLocaleString('sr-Latn-RS', {
            day:'numeric',
            month:'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    function reformatDecimalNumbers(article){
        let newAvgPts = parseFloat(article.avg_pts)
        article.avg_pts = newAvgPts.toLocaleString('sr-Latn-RS', {minimumFractionDigits:2, maximumFractionDigits: 2})

        let newSize = parseFloat(article.size)
        article.size = newSize.toLocaleString('sr-Latn-RS', {minimumFractionDigits:2, maximumFractionDigits: 2})

        let newWeight = parseFloat(article.weight)
        article.weight = newWeight.toLocaleString('sr-Latn-RS', {minimumFractionDigits:2, maximumFractionDigits: 2})
    }

    document.getElementById('load_more_button').addEventListener('click', load_more)
})