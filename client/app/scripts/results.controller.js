'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('ResultsController', function ($scope, SteamApi) {
        $scope.data = SteamApi.getData().get({userProfiles: "https://steamcommunity.com/id/razorhg/,http://steamcommunity.com/profiles/76561198045711046/"});

    });
