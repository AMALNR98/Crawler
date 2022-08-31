
function build_lyrics(lyrics) {
    console.log(lyrics.lyrics)
    ret = $(`<p>
    <h4> Lyrics for ${lyrics.name} </h4>
    <h5> <small class="text-muted">${lyrics.artist.name}</small> </h5>
</p>
<p>
    ${lyrics.lyrics}
</p>`)

    return ret;
}

function main() {
    console.log("Hello!!!!!")
    $("a.songLink").click(myfunc)
};

function myfunc(ev) {
    // console.log("Hello world! I am loaded!");
    // $("a.songLink").click(function (ev) {
        console.log(ev.target.href);
        $("div.lyrics").text("Loading ... ");
        $.ajax({url : ev.target.href,
                dataType: 'json',
                success: function(data, textStatus, jqXHR) {
                    $("div.lyrics").html(build_lyrics(data.song));
                    var text = ev.target.innerText;
                    var parent = ev.target.parentNode;
                    $(parent).html(text)
                    $(".song_name")
                    .html(`<a class = "songLink" href="/song/${$(".song_name")
                    .attr("id")}">${$(".song_name").text()}<a/>`);
                     $(".song_name a").click(main);
                     $(".song_name").attr("class", "songs_lyrics");
                     $(parent).attr("class", "song_name");
                }
            });
        ev.preventDefault();
        
}

$(main);