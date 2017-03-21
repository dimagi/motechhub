var http = require('http'),
    httpProxy = require('http-proxy'),
    url = require('url'),
    express = require('express');


class AuthProxy {
  constructor({credentialDatabase}) {
    this.credentialDatabase = credentialDatabase;
    this._proxy = null;
    this.server = null;
    this._app = null;
  }

  get proxy() {
    return this._proxy || (this._proxy = (() => {
      let proxy = httpProxy.createProxyServer({});

      proxy.on('proxyReq', (proxyReq, req, res, options) => {
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

      return proxy;
    })());
  }

  get app() {
    return this._app || (this._app = (() => {
      let app = express();

      app.all(/\w+\/.*/, (req, res) => {
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

      return app;
    })());
  }

  listen() {
    console.log('listening on port 8000');
    this.server = this.app.listen(8000);
    return this;
  }

  stop() {
    console.log('stopping server');
    this.server.close();
    this.server = null;
  }
}

exports.AuthProxy = AuthProxy;
