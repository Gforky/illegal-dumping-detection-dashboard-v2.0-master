var express = require('express')
  , logger = require('morgan')
  , app = express()
  , path = require('path')
  , dashboard = require('jade').compileFile(__dirname + '/source/templates/dashboard.jade')
  , login = require('jade').compileFile(__dirname + '/source/templates/login.jade')
  , operator = require('jade').compileFile(__dirname + '/source/templates/operator.jade')



app.use(logger('dev'))
app.use(express.static(__dirname + '/static'))
app.use(express.static(__dirname + '/bower_components'))
app.use(express.static(__dirname + '/source'))

app.get('/', function (req, res, next) {
  try {
    var html = login({ title: 'Login' })
    res.send(html)
  } catch (e) {
    next(e)
  }
})

app.get('/dashboard', function (req, res, next) {
  try {
    var html = dashboard({ title: 'Dashboard' })
    res.send(html)
  } catch (e) {
    next(e)
  }
})

app.get('/operator', function (req, res, next) {
  try {
    var html = operator({ title: 'Operator To-Do List' })
    res.send(html)
  } catch (e) {
    next(e)
  }
})

app.listen(process.env.PORT || 3000, function () {
  console.log('Listening on http://localhost:' + (process.env.PORT || 3000))
})