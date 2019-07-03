express = require "express"
parse = require "csv-parse"
app = express()
port = 8080

app.use express.static "../app"
app.use express.json()

app.listen port, () ->
  console.log "Listening on port #{port}"

app.post("/email", (req, res) ->
  spawn = require('child_process').spawn
  process = spawn('python', ['./main.py',
    req.query.search, # pass data from
    "2",
    "Data/",
    req.query.email
  ]) # GET method. Example: .../email?search=trump&type=1

  result = ""
  process.stdout.on('data', (data) ->
    result += data.toString()
  )
  process.stdout.on('end', () ->
    console.log "Email task result: #{result}"
    res.send(result)
  )
)

app.get('/test', (req, res)->
  spawn = require('child_process').spawn
  console.log __dirname + "/Data/"
  process = spawn('python', ['./main.py',
    req.query.search, # pass data from
    "1",
    __dirname + "/Data/"
  ]) # GET method. Example: .../test?search=trump&type=1

  result = ""
  process.stdout.on('data', (data) ->
    result += data.toString()
  )
  process.stdout.on('end', () ->
    console.log "JSON result: #{result}"
    res.send(result)
  )
)

test = () ->
  output = []
  parser = parse({
    delimiter: ':'
  })
  parser.on('readable', ()->
    record = undefined
    while (record = parser.read())
      output.push(record)
  )
  parser.on('error', (err)->
    console.error(err.message)
  )
  parser.on('end', ()->{}
  )
  parser.write("root:x:0:0:root:/root:/bin/bash\n")
  parser.write("someone:x:1022:1022::/home/someone:/bin/bash\n")
  parser.end()
  console.log output
test()
