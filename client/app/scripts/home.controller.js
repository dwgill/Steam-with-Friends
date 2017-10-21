'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('HomeController', function ($scope, $state) {        

        $scope.users = [""];
        
        $scope.addNewUser = function() {
            if($scope.users[$scope.users.length - 1] !== ""){
                $scope.users.push('');
            }            
        };
            
        $scope.removeUser = function(index) {
           $scope.users = $scope.users.splice(index, 1);
        };

        $scope.userInput = function(index, value) {
            $scope.users[index] = value;
        }

        $scope.search = function() {
            $state.go("results", {"users":"$scope.users"});
        };
    });

