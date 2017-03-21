var http = require('http'),
    https = require('https'),
    httpProxy = require('http-proxy'),
    url = require('url'),
    express = require('express'),
    bodyParser = require('body-parser'),
    fs = require('fs');


class AuthProxy {
  constructor({credentialDatabase, ssl = null}) {
    this.credentialDatabase = credentialDatabase;
    this._proxy = null;
    this.server = null;
    this._app = null;
    this.ssl = ssl;
  }

  get proxy() {
    return this._proxy || (this._proxy = (() => {
      let proxy = httpProxy.createProxyServer();

      proxy.on('proxyReq', (proxyReq, req, res, options) => {
        let token = req.url.split('/')[1];
        let endpoint = options._endpoint;
        delete options._endpoint;
        console.log(req.headers['host']);

        proxyReq.path = '/' + req.url.split('/').slice(2).join('/');
        proxyReq.setHeader('host', url.parse(endpoint.target).host);
        if (endpoint.auth.method === 'basic') {
          let authString = endpoint.auth.username + ':' + endpoint.auth.password;
          proxyReq.setHeader('authorization', 'Basic ' + (new Buffer(authString).toString('base64')));
        } else if (endpoint.auth.method === 'apikey') {
          let authString = endpoint.auth.username + ':' + endpoint.auth.apikey;
          proxyReq.setHeader('authorization', 'ApiKey ' + authString);
        }

        console.log(`${proxyReq.method} ${proxyReq.getHeader('host')}${proxyReq.path}`);
      });

      return proxy;
    })());
  }

  get app() {
    return this._app || (this._app = (() => {
      let app = express();

      app.use(function (err, req, res, next) {
        console.error(err.stack);
        res.status(500).send('Something broke!')
      });

      app.all(/\w+\/.*/, (req, res) => {
        let token = req.url.split('/')[1];
        this.credentialDatabase.get(token, (err, endpoint) => {
          if (err && err.statusCode === 404) {
            res.status(404).end();
          } else if (err && err.name == "Decryption Error") {
            res.status(500).send("Could not decrypt credentials");
          } else if (err) {
            res.status(500).end();
          } else {
            this.proxy.web(req, res, {target: endpoint.target, secure: false, _endpoint: endpoint});
          }
        });
      });

      app.route('/:token')
        .head((req, res, next) => {
          let token = req.params.token;
          this.credentialDatabase.has(token, (err, hasToken) => {
            res.setHeader('content-length', 0);
            res.status(hasToken ? 200 : 404).end();
          });
        })
        .put(bodyParser.json(), (req, res) => {
          let token = req.params.token;
          let credential = req.body;
          if (!credential.target) {
            res.status(400).send("Your credential must contain a 'target' property").end();
          }
          this.credentialDatabase.set(token, credential, (err) => {
            res.status(err ? 500 : 200).end();
          });
        })
        .delete((req, res) => {
          let token = req.params.token;
          this.credentialDatabase.clear(token, (err) => {
            res.status(err ? 500 : 200).end();
          });
        });

      return app;
    })());
  }

  listen() {
    console.log('listening on port 8000');
    if (this.ssl) {
      this.server = https.createServer(this.ssl, this.app).listen(8000);
    } else {
      this.server = http.createServer(this.app).listen(8000);
    }
    return this;
  }

  stop() {
    console.log('stopping server');
    this.server.close();
    this.server = null;
  }
}

exports.AuthProxy = AuthProxy;
