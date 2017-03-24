var http = require('http'),
    httpAuth = require('http-auth');

class DummyServer {
  constructor({port, username, password}) {
    this.port = port;
    this.username = username;
    this.password = password;

    if (username && password) {
      var basic = httpAuth.basic({realm: "Dummy Realm"}, this.handleBasicAuth.bind(this));
      this.server = http.createServer(basic, this.handleCreateServer.bind(this));
    } else {
      this.server = http.createServer(this.handleCreateServer.bind(this));
    }
  }

  handleBasicAuth(username, password, callback) {
    callback(username === this.username && password === this.password);
  }

  handleCreateServer(req, res) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.write(JSON.stringify({
      url: req.url,
      headers: req.headers,
      method: req.method,
    }, true, 2));
    res.end();
  }

  listen() {
    console.log(`listening on port ${this.port}`);
    this.server.listen(this.port);
    return this;
  }

  stop() {
    this.server.close()
  }
}

exports.DummyServer = DummyServer;


if (require.main == module) {
  new DummyServer({port: 9000, username: 'admin', password: '123'}).listen()
}
