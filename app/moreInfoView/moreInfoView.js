'use strict';

angular.module('myApp.moreInfoView', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/moreInfo', {
    templateUrl: 'moreInfoView/moreInfoView.html',
    controller: 'moreInfoViewCtrl'
  });
}])

.controller('moreInfoViewCtrl', [function() {

}]);