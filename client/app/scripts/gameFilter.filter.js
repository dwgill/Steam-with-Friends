angular
.module('steam-with-friends')
.filter('gameFilter', function () {
    return function(games, tags, genres) {
        if(games && games.length > 0){
            var tagsArray = tags.map(function(tag){
                return tag.text;
            });
            var genresArray = genres.map(function(genre){
                return genre.text;
            });
            return games.filter(function(game){
                return (tags.length === 0 || _.intersection(game.tags, tagsArray).length === tags.length) && 
                        (genres.length === 0 || _.intersection(game.genres, genresArray).length === genres.length);
            });
        }
       
    };
});