'use strict';
// books and news api

// alert('book and news api js loaded')
const bookUrl = `https://www.googleapis.com/books/v1/volumes?q=rental+property&key=${GG_KEY}`
window.onload = function getBooksAndNews() {
    console.log('==========booksapi is being called============')
    fetch(bookUrl).then((response) => response.json())
        .then((data) => {
            for (let i = 0; i < 8; i++) {
                console.log(data);
                // console.log(`this is the link ${data.items[i].volumeInfo.industryIdentifiers.infoLink}`)
                const book_card =
                    '<div id="book_card" class="col-6 col-lg-3 mb-4">' +
                    '<a href=' + data.items[i].volumeInfo.infoLink + ' target="_blank"><img src=' + data.items[i].volumeInfo.imageLinks.thumbnail + ' alt="book-cover" class="img-fluid"></a>' +
                    '</div>'
                document.querySelector('#book').insertAdjacentHTML('beforeend', book_card)
            }
        });

    // adding get_news here as well because cannot have two window.onload functions
    const url = `https://newsapi.org/v2/everything?q=rental+property+investment+real+estate+mortgage&sortBy=relevancy&apiKey=${API_KEY}`
    fetch(url).then((response) => response.json())
        .then((data) => {
            for (let i = 0; i < 2; i++) {
                // console.log(data);
                console.log("urlToImage: " + data.articles[i].urlToImage);
                if ('urlToImage' in data.articles[i]) {
                    const news_card = '<div class="col-md-6 p-3">' +
                        '<div class="card" id="card-news">' +
                        '<img id="news-img" src=' + data.articles[i].urlToImage + ' alt="photo-from-news" class="card-img-top">' +
                        '<div class="card-body">' +
                        '<h4 class="card-title" id="news-title">' + data.articles[i].title.slice(0, 100) + '</h4>' +
                        '<p class="card-text" id="news-text"></p>' +
                        data.articles[i].content.slice(0, 200) + '<br>' +
                        '<a href=' + data.articles[i].url + 'id="news-link" class="btn btn-lg btn-success rounded-pill mt-2" target="_blank"  >Read more</a>' +
                        '</div>' +
                        '</div>' +
                        '</div>'
                    document.querySelector('#news_container').insertAdjacentHTML('beforeend', news_card)
                }
            }
        });
    // get quotes
    fetch('/quotes.json').then((response) => response.json())
        .then((allQuotes) => {
            console.log(allQuotes);
            console.log(Object.keys(allQuotes).length);
            let randomPos = Math.floor(Math.random() * allQuotes.quotes.length) - 1;
            let randomQuote = allQuotes.quotes[randomPos];
            let author = (Object.keys(randomQuote))[0];
            let quote = (Object.values(randomQuote))[0];
            document.querySelector('#quote').innerText = quote;
            document.querySelector('#author').innerText = author;
        });

    // quotes above

}