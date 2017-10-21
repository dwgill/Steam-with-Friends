'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('ResultsController', function ($scope, SteamApi, $state) {
        
        var ids = $state.params.users.map(function(user){
            return user.id;
        }).toString();

        SteamApi.getData().get({users: ids}).$promise.then(function(response){
            $scope.data = response.users;
            
            $scope.commonGames =  response.games;
        });
        
    });
