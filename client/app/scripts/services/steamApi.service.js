'use strict';

angular.module('steam-with-friends')
    .service('SteamApi', function ($resource) {
        function getData(){
            return $resource('http://localhost:5000/get-games');
        }

        return {
            getData: getData
        };
    });
