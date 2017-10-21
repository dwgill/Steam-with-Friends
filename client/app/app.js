'use strict';

angular.module('steam-with-friends', [
    'ngResource',
    'ngSanitize',
    'ui.router'
]);
angular.module('steam-with-friends').run();

angular.module('steam-with-friends').config(function($urlRouterProvider, $stateProvider, $locationProvider){
    $locationProvider.html5Mode(true);
    var basePath = window.location.pathname.split('/')[1];
    var slash = basePath ? "/" : "";
    $stateProvider.state('home', {
        url: slash + 'home',
        views:{
            body:{
                templateUrl: 'home.html',
                controller: 'HomeController'
            }
        }
        
    });

    $urlRouterProvider
    .when('/home', function ($state) {
        $state.go('home');
    })
    .otherwise(function ($injector) {
        var $state = $injector.get('$state');
        $state.go('home');
    });
});


