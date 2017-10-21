'use strict';
/* global _*/

angular.module('steam-with-friends')

    .controller('HomeController', function ($scope, $state) {        

        $scope.users = [{id: ''}];
        
        $scope.addNewUser = function() {
            if($scope.users[$scope.users.length - 1].id !== ""){
                $scope.users.push({id:''});
            }            
        };
            
        $scope.removeUser = function(index) {
            if(index > 0){
                $scope.users = $scope.users.splice(index, 1);
            }
           
        };


        $scope.search = function() {
            $scope.users = $scope.users.filter(function(user){ return user.id  !== '';});
            $state.go("results", {users: $scope.users});
        };
    });

