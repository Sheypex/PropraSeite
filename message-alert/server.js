var express = require('express');
var app = express();

app.listen(8080, function () {
  console.log('server running on port 8080');
})

app.set('views', __dirname);
app.get('/test', execute);

function execute(req, res) {
  var spawn = require('child_process').spawn;
  var process = spawn('python', ['./main.py',
    req.query.search, // pass data from
    req.query.type
  ]); // GET method. Example: .../test?search=trump&type=1

  var result = "";
  process.stdout.on('data', function (data) {
    result += data.toString()
  });

  process.stdout.on('end', function() {
    res.send(result);
    });
}
