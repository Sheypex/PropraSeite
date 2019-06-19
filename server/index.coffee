express = require "express"
parse = require "csv-parse"
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
  process.stdout.on('end', () ->
    console.log result
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
