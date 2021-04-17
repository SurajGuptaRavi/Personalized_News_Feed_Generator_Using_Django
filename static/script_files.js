$(document).ready(function() {

    $(".nav-tabs a").click(function() {
        $(this).tab('show');


    });
    $('.main-carousel').flickity({
        // options
        cellAlign: 'left',
        contain: true
    });
});

// Script for liking the articles
function Like_This_Article(article_id) {
    var xhttp;
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('Article added to watch');
        }
    };
    xhttp.open("GET", "/like_article?article_id=" + String(article_id), true);
    xhttp.send();
};

// Script for Saving the articles
function Save_This_Article(article_id) {
    var xhttp;
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('Article added to watch');
        }
    };
    xhttp.open("GET", "/save_article?article_id=" + String(article_id), true);
    xhttp.send();
};

// Script for saving the count of Sharing  articles
function Share_This_Article(article_id) {
    var xhttp;
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('Article added to watch');
        }
    };
    xhttp.open("GET", "/share_article?article_id=" + String(article_id), true);
    xhttp.send();
};


// Code for Adding to Watch later 
function AddToHitory(article_id) {
    var xhttp;
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('Article added to watch');
        }
    };
    xhttp.open("GET", "/add_to_history?article_id=" + String(article_id), true);
    xhttp.send();
};