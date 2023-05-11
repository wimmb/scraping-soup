/*
    Scripts
*/

function scrapeData(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function() {
            alert("Data Scraped!");
        },
        error: function() {
            alert("Error calling API");
        }
    });
}

$(document).ready(function() {
    $("#scrape_movies_btn").click(function() {
        var url = $(this).data("url");
        scrapeData(url);
    });

    $("#scrape_tv_shows_btn").click(function() {
        var url = $(this).data("url");
        scrapeData(url);
    });
});