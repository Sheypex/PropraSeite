#'use strict';

angular.module('myApp.homeView', ['ngRoute'])
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider.when '/', {
      templateUrl: 'homeView/homeView.html',
      controller: 'View1Ctrl'
    }
])
  .controller('View1Ctrl', [() ->
    demo()
  ])

demo = () ->
  test =
    hallo: 5
    fast: "Da"
  opt =
    method: "POST"
    headers:
      "Content-Type": "application/json"
    body: JSON.stringify(test)

  res = await fetch "http://localhost:4017/test", opt
  data = await res.json()
  console.log data
