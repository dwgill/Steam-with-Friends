'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('ResultsController', function ($scope, SteamApi) {
        function mapGames(userInfos){
            return userInfos.map(function(userInfo){
                return userInfo.games;
            });
        }
        SteamApi.getData().get({userProfiles: "https://steamcommunity.com/id/razorhg/,http://steamcommunity.com/profiles/76561198045711046/"}).$promise.then(function(response){
            $scope.data = response;
            var games = mapGames(response);
            $scope.commonGames =  _.intersectionBy(games[0], games[0], games[1], 'appid');
        });
        
    });
