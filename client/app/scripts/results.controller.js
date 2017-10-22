'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('ResultsController', function ($scope, SteamApi, $state, $location) {
        $scope.tags = [];
        $scope.genres = [];
        $scope.selectedTags = [];
        $scope.selectedGenres = [];
        if($state.params.users && $state.params.users.length ){
            SteamApi.getData().get({users: $state.params.users.toString()}).$promise.then(function(response){
                $scope.data = response.users;
                $scope.gamesLoaded = true;
                $scope.tags = _.reduce(response.games, function(tags, game){
                    return _.union(tags, game.tags);
                }, []);
                $scope.genres = _.reduce(response.games, function(genres, game){
                    return _.union(genres, game.genres);
                }, []);
                $scope.commonGames =  response.games;
            });
        } else{
            $state.go('home');
        }
        
        $scope.goBack = function(){
            $state.go('home', {users: $state.params.users});
        };

        $scope.moreDetails = function(game){
            game.span = game.span === 2 ? 1 : 2;
        };

        $scope.listItems = function(items){
            return items.join(" ");
        };
        
    });
