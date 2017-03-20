var http = require('http'),
    httpProxy = require('http-proxy'),
    url = require('url');


class AuthProxy {
  constructor({credentialDatabase}) {
    this.credentialDatabase = credentialDatabase;
    this.proxy = null;
    this.server = null;
    this.init();
  }

  init() {
    this.proxy = httpProxy.createProxyServer({});

    this.proxy.on('proxyReq', (proxyReq, req, res, options) => {
      let token = req.url.split('/')[1];
      let endpoint = options._endpoint;
      delete options._endpoint;

      proxyReq.path = '/' + req.url.split('/').slice(2).join('/');
      proxyReq.setHeader('host', url.parse(endpoint.target).host);
      if (endpoint.username) {
        let authString = endpoint.username + ':' + endpoint.password;
        proxyReq.setHeader('authorization', 'Basic ' + (new Buffer(authString).toString('base64')));
      }

      console.log(proxyReq.getHeader('host'), proxyReq.path);
    });
    this.server = http.createServer((req, res) => {
      let token = req.url.split('/')[1];
      this.credentialDatabase.get(token, (err, endpoint) => {
        if (err && err.statusCode === 404) {
          res.statusCode = 404;
          res.end();
        } else if (err) {
          res.statusCode = 500;
        } else {
          this.proxy.web(req, res, {target: endpoint.target, secure: endpoint.secure, _endpoint: endpoint});
        }
      });
    });
  }

  listen() {
    console.log('listening on port 8000');
    this.server.listen(8000);
    return this;
  }

  stop() {
    console.log('stopping server');
    this.server.close()
  }
}

exports.AuthProxy = AuthProxy;
