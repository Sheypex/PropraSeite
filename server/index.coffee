express = require "express"
app = express()
port = 8080

app.use express.static "../app"
app.use express.json()

app.listen port, () ->
  console.log "Listening on port #{port}"

app.get('/test', (req, res)->
  spawn = require('child_process').spawn
  process = spawn('python', ['./main.py',
    req.query.search, # pass data from
    req.query.type
  ]) # GET method. Example: .../test?search=trump&type=1

  result = ""
  process.stdout.on('data', (data) ->
    result += data.toString()
  )
  console.log "here"
  process.stdout.on('end', () ->
    console.log result
    res.send(result)
  )
)

