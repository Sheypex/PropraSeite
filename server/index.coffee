express = require "express"
app = express()
port = 4017

app.use express.static "../app"
app.use express.json()

app.get "/kA", (req, res) ->
  res.send "Timestamp: " + Date.now()

app.listen port, () ->
  console.log "Listening on port #{port}"

app.post "/test", (req, res) ->
  console.log req
  console.log req.body
  res.json({
    status: "succ"
    test: 5
    jetzt: "Hier"
  })


