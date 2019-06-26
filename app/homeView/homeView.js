// Generated by CoffeeScript 2.4.1
(function() {
  //'use strict'
  var checkDateLength, getDateFormat, plotBubbleChart, plotTerm, queryTopic, sendEmail, separateData, updateGraphs;

  angular.module('myApp.homeView', ['ngRoute']).config([
    '$routeProvider',
    function($routeProvider) {
      return $routeProvider.when('/',
    {
        templateUrl: 'homeView/homeView.html',
        controller: 'View1Ctrl'
      });
    }
  ]).controller('View1Ctrl', [
    "$scope",
    function($scope) {
      $scope.topics = ["Trump",
    "Klimawandel",
    "FakeNews"];
      $scope.topic = $scope.topics[0];
      $scope.showTerm = true;
      $scope.showCounted = true;
      $scope.showTopUser = true;
      $scope.showSentiment = true;
      $scope.selectTopic = function(topic) {
        $scope.topic = topic;
        updateGraphs($scope,
    $scope.topic);
        console.log(topic);
        console.log($scope.showTerm);
        console.log($scope.showCounted);
        console.log($scope.showTopUser);
        return console.log($scope.showSentiment);
      };
      
      $scope.userEmail = "";
      $scope.sendEmail = function() {
        return sendEmail($scope.topic,
    $scope.userEmail);
      };
      
      $scope.topicQuery = "";
      $scope.queryTopic = function() {
        $scope.topic = $scope.topicQuery;
        return queryTopic($scope,
    $scope.topicQuery);
      };
      
      return updateGraphs($scope,
    $scope.topic);
    }
  ]);

  queryTopic = function(scope, topic) {
    return updateGraphs(scope, topic, "query");
  };

  sendEmail = function(topic, userEmail) {
    return fetch(`http://localhost:8080/email?search=${topic}&email=${userEmail}`, {
      method: "POST"
    });
  };

  updateGraphs = function(scope, topic, url = "static") {
    if (url === "static") {
      url = `http://localhost:8080/test?search=${topic}&type=1`;
    } else if (url === "query") {
      url = `https://giant-firefox-64.localtunnel.me/test?search=${topic}`;
    } else {
      return -1;
    }
    return fetch(url, {
      mode: 'cors'
    }).then(function(response) {
      console.log(response);
      return response.text();
    }).then(function(text) {
      console.log(text);
      return separateData(scope, JSON.parse(text));
    }).catch(function(error) {
      return console.log('Request failed', error);
    });
  };

  getDateFormat = function(date) {
    return date.getFullYear() + "-" + checkDateLength(date.getMonth() + 1) + "-" + checkDateLength(date.getDate()) + " " + checkDateLength(date.getHours()) + ":" + checkDateLength(date.getMinutes()) + ":" + checkDateLength(date.getSeconds());
  };

  checkDateLength = function(dateLength) {
    if (dateLength < 10) {
      return "0" + dateLength;
    } else {
      return dateLength;
    }
  };

  plotTerm = function(xData, yData, graphName, xName, yName, type) {
    var layout, termData, trace1;
    trace1 = {
      x: xData,
      y: yData,
      type: 'line',
      name: graphName
    };
    layout = {
      title: {},
      xaxis: {
        title: {
          text: xName,
          font: {
            family: 'Courier New, monospace',
            size: 18,
            color: '#7f7f7f'
          }
        }
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
    };
    termData = [trace1];
    return Plotly.newPlot(type, termData, layout);
  };

  plotBubbleChart = function(xData, yData, hashtags, size, type) {
    var data, layout, trace1;
    trace1 = {
      x: xData,
      y: yData,
      text: hashtags,
      mode: 'markers+text',
      textposition: 'center',
      marker: {
        size: size
      }
    };
    data = [trace1];
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
    };
    return Plotly.newPlot(type, data, layout);
  };

  separateData = function(scope, data) {
    var count, countedData, hashtags, sentimentsData, size, size2, termsData, topUser, topUserData, xCounted, xSentiment, xTerm, xTopUser, yCounted, ySentiment, yTerm, yTopUser;
    // terms Data
    termsData = data.result.term;
    if (termsData !== "no_data") {
      xTerm = [];
      yTerm = [];
      Object.keys(termsData).forEach(function(key) {
        var xDate;
        xDate = new Date(parseFloat(key));
        xTerm.push(getDateFormat(xDate));
        return yTerm.push(termsData[key]);
      });
      plotTerm(xTerm, yTerm, 'Tweets Loaded', 'Dates', 'Number of Tweets', 'term');
    }
    // counted Data
    countedData = data.result.counted;
    if (countedData !== "no_data") {
      count = 1;
      xCounted = [];
      yCounted = [];
      hashtags = [];
      size = [];
      Object.keys(countedData).forEach(function(key) {
        xCounted.push(count++);
        yCounted.push(countedData[key][1]);
        size.push(countedData[key][1] * 4);
        return hashtags.push(countedData[key][0]);
      });
      plotBubbleChart(xCounted, yCounted, hashtags, size, "counted");
    }
    // topUser Data
    topUserData = data.result.topuser;
    if (topUserData !== "no_data") {
      count = 1;
      xTopUser = [];
      yTopUser = [];
      topUser = [];
      size2 = [];
      Object.keys(topUserData).forEach(function(key) {
        xTopUser.push(count++);
        yTopUser.push(topUserData[key][1]);
        size2.push(topUserData[key][1] * 4);
        return topUser.push(topUserData[key][0]);
      });
      plotBubbleChart(xTopUser, yTopUser, topUser, size2, "topuser");
    }
    // Sentiment Data
    sentimentsData = data.result.sentiment;
    if (sentimentsData !== "no_data") {
      xSentiment = [];
      ySentiment = [];
      sentimentsData.forEach(function(element) {
        xSentiment.push(element.Time);
        return ySentiment.push(element.Sentiment);
      });
      plotTerm(xSentiment, ySentiment, "Sentiment Analisis", "Dates", "Sentiment", "sentiment");
    }
    return scope.$apply(function() {
      scope.showTerm = termsData !== "no_data";
      scope.showCounted = countedData !== "no_data";
      scope.showTopUser = topUserData !== "no_data";
      return scope.showSentiment = sentimentsData !== "no_data";
    });
  };

}).call(this);

//# sourceMappingURL=homeView.js.map
