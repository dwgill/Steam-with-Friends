'use strict';

angular.module('steam-with-friends', [
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ui.router'
]);
angular.module('steam-with-friends').run();

angular.module('steam-with-friends').config(function($urlRouterProvider, $stateProvider){
    var basePath = window.location.pathname.split('/')[1];
    var slash = basePath ? "/" : "";
    $stateProvider.state('home', {
        abstract: true,
        url: slash + basePath,
        views: {
            'body': {templateUrl: 'home.html'}
        
        }
    });
});


