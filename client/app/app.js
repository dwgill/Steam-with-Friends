'use strict';

angular.module('steam-with-friends', [
    'ngResource',
    'ngSanitize',
    'ui.router',
    'ui.bootstrap',
    'ngMaterial'
]);
angular.module('steam-with-friends').run();

angular.module('steam-with-friends').config(function($urlRouterProvider, $stateProvider, $locationProvider){
    $locationProvider.html5Mode(true);
    var basePath = window.location.pathname.split('/')[1];
    var slash = basePath ? "/" : "";
    $stateProvider.state('home', {
        url: slash + 'home?users',
        views:{
            body:{
                templateUrl: 'home.html',
                controller: 'HomeController'
            }
        }
        
    }).state('results', {
        url: slash + 'results?users',
        views:{
            body:{
                templateUrl: 'results.html',
                controller: 'ResultsController'
            }
        }
        
    });

    $urlRouterProvider
    .when('/home', function ($state) {
        $state.go('home');
    })
    .when('/results', function ($state, $location) {
        $state.go('results');
        
        
    })
    .otherwise(function ($injector) {
        var $state = $injector.get('$state');
        $state.go('home');
    });
});


