
//nav bar and side bar
var menuIcon = document.querySelector(".menu_icon")
var sidebar = document.querySelector(".sidebar")
var content = document.querySelector(".content")





menuIcon.onclick =function(){
    sidebar.classList.toggle("small-sidebar")
    content.classList.toggle("large-content")
}


document.querySelector(".logo").addEventListener("click", () => {
    window.location.href = "index.html";
});


// -----------------------------------



//poster extract from title

function getPoster(){

     let film = document.getElementById("term").getAttribute('value');
     console.log(film);
     

          $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=" + film + "&callback=?", function(json) {
             if (json != "Nothing found."){                 
console.log(json);
                $('#poster').html( '<img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
            } 
            else{
                    $('#poster').html( '<img src=\"static/thumbnail1.png' + json.results[0].poster_path + '\" class=\"img-responsive\" >');

                }
           });

        

      return false;
 }

//  getPoster();

