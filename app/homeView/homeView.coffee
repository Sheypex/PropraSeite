#'use strict'

angular.module('myApp.homeView', ['ngRoute'])
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider.when '/', {
      templateUrl: 'homeView/homeView.html',
      controller: 'View1Ctrl'
    }
])
  .controller('View1Ctrl', ["$scope", ($scope) ->
    $scope.topics = ["Trump", "Klimawandel", "FakeNews"]
    $scope.topic = $scope.topics[0]
    $scope.showTerm = true
    $scope.showCounted = true
    $scope.showTopUser = true
    $scope.showSentiment = true
    $scope.selectTopic = (topic) ->
      $scope.topic = topic
      updateGraphs($scope, $scope.topic)
      console.log topic
      console.log $scope.showTerm
      console.log $scope.showCounted
      console.log $scope.showTopUser
      console.log $scope.showSentiment
    #
    $scope.userEmail = ""
    $scope.sendEmail = () ->
      sendEmail($scope.topic, $scope.userEmail)
    #
    $scope.topicQuery = ""
    $scope.queryTopic = () ->
      $scope.topic = $scope.topicQuery
      queryTopic($scope, $scope.topicQuery)
    #
    updateGraphs($scope, $scope.topic)
])

queryTopic = (scope, topic) ->
  updateGraphs(scope, topic, "query")

sendEmail = (topic, userEmail) ->
  fetch("http://localhost:8080/email?search=#{topic}&email=#{userEmail}", {method: "POST"})

updateGraphs = (scope, topic, url="static") ->
  if (url == "static") then url = "http://localhost:8080/test?search=#{topic}&type=1"
  else if (url == "query") then  url = "https://giant-firefox-64.localtunnel.me/test?search=#{topic}"
  else return -1

  fetch(url, {mode: 'cors'})
    .then((response) ->
      console.log(response)
      response.text()
    )
    .then((text) ->
      console.log(text)
      separateData(scope, JSON.parse(text))
    )
    .catch((error) ->
      console.log('Request failed', error)
    )

getDateFormat = (date) ->
  return date.getFullYear() + "-" + checkDateLength(date.getMonth() + 1) + "-" + checkDateLength(date.getDate()) + " " + checkDateLength(date.getHours()) + ":" + checkDateLength(date.getMinutes()) + ":" + checkDateLength(date.getSeconds())

checkDateLength = (dateLength) ->
  if (dateLength < 10) then return "0" + dateLength else return dateLength

plotTerm = (xData, yData, graphName, xName, yName, type) ->
  trace1 = {
    x: xData,
    y: yData,
    type: 'line',
    name: graphName
  }
  layout = {
    title: {
    },
    xaxis: {
      title: {
        text: xName,
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
    },
    yaxis: {
      title: {
        text: yName,
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      }
    }
  }
  termData = [trace1]
  Plotly.newPlot(type, termData, layout)

plotBubbleChart = (xData, yData, hashtags, size, type) ->
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


separateData = (scope, data) ->
  # terms Data
  termsData = data.result.term
  if termsData isnt "no_data"
    xTerm = []
    yTerm = []
    Object.keys(termsData).forEach((key) ->
      xDate = new Date(parseFloat(key))
      xTerm.push(getDateFormat(xDate))
      yTerm.push(termsData[key])
    )
    plotTerm(xTerm, yTerm, 'Tweets Loaded', 'Dates', 'Number of Tweets', 'term')

  # counted Data
  countedData = data.result.counted
  if countedData isnt "no_data"
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
    plotBubbleChart(xCounted, yCounted, hashtags, size, "counted")

  # topUser Data
  topUserData = data.result.topuser
  if topUserData isnt "no_data"
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
    plotBubbleChart(xTopUser, yTopUser, topUser, size2, "topuser")

  # Sentiment Data
  sentimentsData = data.result.sentiment
  if sentimentsData isnt "no_data"
    xSentiment = []
    ySentiment = []
    sentimentsData.forEach((element) ->
      xSentiment.push(element.Time)
      ySentiment.push(element.Sentiment)
    )
    plotTerm(xSentiment, ySentiment, "Sentiment Analisis", "Dates", "Sentiment", "sentiment")

  scope.$apply(() ->
    scope.showTerm = (termsData isnt "no_data")
    scope.showCounted = (countedData isnt "no_data")
    scope.showTopUser = (topUserData isnt "no_data")
    scope.showSentiment = (sentimentsData isnt "no_data")
  )

