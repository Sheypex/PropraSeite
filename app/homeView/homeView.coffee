#'use strict'

angular.module('myApp.homeView', ['ngRoute'])
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider.when '/', {
      templateUrl: 'homeView/homeView.html',
      controller: 'View1Ctrl'
    }
])
  .controller('View1Ctrl', ["$scope",($scope) ->
    $scope.topics = ["Trump", "Klimawandel", "FakeNews"]
    $scope.topic = $scope.topics[0]
    $scope.selectTopic = (topic) ->
      $scope.topic = topic
      updateGraphs($scope.topic)
      console.log topic
  #
    updateGraphs($scope.topic)

  ])

updateGraphs = (topic) ->
  url = "http://localhost:8080/test?search=#{topic}&type=1"
  fetch(url, {mode: "no-cors"}).then((response) ->
    response.json()
  )
    .then((result) ->
      console.log('success:', result)
      div = document.getElementById('test')
      div.innerHTML = "title: #{result.title}<br/>message: #{result.message}"
    )
    .catch((error) -> console.log('error:', error))

  separateData()

getDateFormat= (date) ->
  return date.getFullYear() + "-" + checkDateLength(date.getMonth() + 1) + "-" + checkDateLength(date.getDate()) + " " + checkDateLength(date.getHours()) + ":" + checkDateLength(date.getMinutes()) + ":" + checkDateLength(date.getSeconds())

checkDateLength=(dateLength) ->
  if (dateLength < 10) then return "0" + dateLength
  else return dateLength

plotTerm=(xData, yData) ->
  trace1 = {
    x: xData,
    y: yData,
    type: 'line',
    name: 'Trump Tweets Loaded'
  }
  layout = {
    title: {},
    xaxis: {
      title: {
        text: 'Dates',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
    },
    yaxis: {
      title: {
        text: 'Number of Tweets',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      }
    }
  }
  termData = [trace1]
  Plotly.newPlot('term', termData, layout)


plotBubbleChart= (xData, yData, hashtags, size, type) ->
  trace1 = {
    x: xData,
    y: yData,
    text: hashtags,
    mode: 'markers+text',
    textposition: 'center',
    marker: {
      size: size,
    }
  }
  data = [trace1]
  layout = {
    colorway: ['#0497f3', 'rgba(34,28,28,0.82)'],
    showlegend: false,
    font: {
      family: 'Courier New, monospace',
      size: 15,
      color: '#222222'
    },
    xaxis: {
      autorange: true,
      showgrid: false,
      zeroline: false,
      showline: false,
      autotick: false,
      ticks: '',
      showticklabels: false
    },
    yaxis: {
      autorange: true,
      showgrid: false,
      zeroline: true,
      showline: true,
      autotick: true,
      ticks: '',
      showticklabels: true
    }
  }
  Plotly.newPlot(type, data, layout)

loadData= ()->
# TODO: This should be loaded from the node.js server
  jsonString = "{\"result\":{\"term\":{\"1558213200000\":16896,\"1558216800000\":1,\"1558220400000\":0,\"1558224000000\":0,\"1558227600000\":1,\"1558231200000\":0,\"1558234800000\":0,\"1558238400000\":0,\"1558242000000\":0,\"1558245600000\":0,\"1558249200000\":0,\"1558252800000\":0,\"1558256400000\":0,\"1558260000000\":0,\"1558263600000\":193},\"counted\":[[\"#BREAKING\",5],[\"#moms\",6],[\"#EEUU\",6],[\"#toddlers\",6],[\"#MAGAmemes\",7],[\"#maga\",7],[\"#WAKEUPAMERICA\",8],[\"#RT\",13],[\"#trump\",14],[\"#FAUXnews\",14],[\"#ccot\",17],[\"#tcot\",30],[\"#kag\",33],[\"#NATO\",35]],\"topuser\":[[\"bettyblack176\",11],[\"all_sabrina\",11],[\"MaryFabulous3\",11],[\"lpbrown7\",12],[\"AmericanMom2\",12],[\"ProfSchlitzo7\",12],[\"Pasha_Enrik\",12],[\"trilingual1946\",12],[\"FLpalmtree1\",12],[\"minamoradi2020\",12],[\"BarleyFields1\",12],[\"AJHolland01\",13],[\"sueludad\",13],[\"spooner_lindsay\",13],[\"rawlings_cindy\",13],[\"Sekusa1\",13],[\"atypicalblonde\",14],[\"Pissed_Woman\",14],[\"JeffreyHardin15\",14],[\"kathy_levy\",15],[\"primfreak\",15],[\"gnod111\",16],[\"SearchingForTr9\",16],[\"Eyerish13\",16],[\"GymCoachMac\",17]]}}"
  return JSON.parse(jsonString)

separateData= () ->
  data = loadData()

  # terms Data
  termsData = data.result.term
  xTerm = []
  yTerm = []
  Object.keys(termsData).forEach((key) ->
    xDate = new Date(parseFloat(key))
    xTerm.push(getDateFormat(xDate))
    yTerm.push(termsData[key])
  )

  # counted Data
  countedData = data.result.counted
  count = 1
  xCounted = []
  yCounted = []
  hashtags = []
  size = []
  Object.keys(countedData).forEach((key) ->
    xCounted.push(count++)
    yCounted.push(countedData[key][1])
    size.push(countedData[key][1] * 4)
    hashtags.push(countedData[key][0])
  )

  # topUser Data
  topUserData = data.result.topuser
  count = 1
  xTopUser = []
  yTopUser = []
  topUser = []
  size2 = []
  Object.keys(topUserData).forEach((key) ->
    xTopUser.push(count++)
    yTopUser.push(topUserData[key][1])
    size2.push(topUserData[key][1] * 4)
    topUser.push(topUserData[key][0])
  )

  # plot all the data  and visualize it
  plotTerm(xTerm, yTerm)
  plotBubbleChart(xCounted, yCounted, hashtags, size, "counted")
  plotBubbleChart(xTopUser, yTopUser, topUser, size2, "topuser")
