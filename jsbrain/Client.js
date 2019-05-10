const zerorpc = require('zerorpc')
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

module.exports.client = client;
