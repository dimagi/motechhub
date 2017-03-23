/*globals describe, it, expect, beforeAll, afterAll */
let Crypto = require('../crypto.js').Crypto;
let CredentialDatabase = require('../credential-database.js').CredentialDatabase;
let AuthProxy = require('../authproxy.js').AuthProxy;
let DummyServer = require('../dummyserver.js').DummyServer;
let request = require('request');


describe("Auth Proxy's ability to proxy", () => {
  let authProxy, dummyServer, token, tokenPassword, credentialDatabase;

  tokenPassword = 'XYZ';

  beforeAll(() => {
    credentialDatabase = new CredentialDatabase({
      dbUri: 'http://localhost:5984',
      dbName: 'test_authproxy',
      crypto: new Crypto('*** secret password ***'),
    });
    token = 'c7de095ee07e4e1be55594d6d2ba4676';
    authProxy = new AuthProxy({credentialDatabase}).listen();
    dummyServer = new DummyServer({port: 9000, username: 'admin', password: '123'}).listen();
  });

  beforeAll((done) => {
    credentialDatabase.set(token, tokenPassword, {
      target: 'http://localhost:9000',
      auth: {
        method: 'basic',
        username: 'admin',
        password: '123'
      }
    }, () => {
      done();
    });
  });

  afterAll(() => {
    authProxy.stop();
    dummyServer.stop();
  });

  it("lets you proxy GET using basic auth", (done) => {
    request.get({
      url: 'http://localhost:8000/c7de095ee07e4e1be55594d6d2ba4676/hello',
      headers: {'x-authproxy-token-password': tokenPassword},
    }, function(error, response, body) {
      expect(JSON.parse(body)).toEqual({
        "url": "/hello",
        "headers": {
          "connection": "close",
          "host": "localhost:9000",
          "authorization": "Basic YWRtaW46MTIz"
        },
        "method": "GET"
      });
      done();
    });
  });

  it("lets you proxy POST using basic auth", (done) => {
    request.post({
      url: 'http://localhost:8000/c7de095ee07e4e1be55594d6d2ba4676/hello',
      headers: {'x-authproxy-token-password': tokenPassword},
    }, function(error, response, body) {
      expect(JSON.parse(body)).toEqual({
        "url": "/hello",
        "headers": {
          "connection": "close",
          "host": "localhost:9000",
          "authorization": "Basic YWRtaW46MTIz",
          "content-length": "0"
        },
        "method": "POST"
      });
      done();
    });
  });
});


describe("Auth Proxy's credential storing API", () => {
  let authProxy, dummyServer, token, credentialDatabase;
  let tokenPassword = 'XYZ';

  beforeAll(() => {
    credentialDatabase = new CredentialDatabase({
      dbUri: 'http://localhost:5984',
      dbName: 'test_authproxy',
      crypto: new Crypto('*** secret password ***'),
    });
    token = '4dfdd3ab2d5a6be04b498dd27cba5259';
    authProxy = new AuthProxy({credentialDatabase}).listen();
  });

  it("will tell you when a credential does not exist", (done) => {
    request.head('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      expect(response.statusCode).toBe(404);
      done();
    });
  });

  it('lets you add a credential', (done) => {
    request.put({
      url: 'http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259',
      json: {target: 'http://localhost:8000', auth: {method: 'none'}},
      headers: {'x-authproxy-token-password': tokenPassword},
    }, (error, response, body) => {
      expect(response.statusCode).toBe(201);
      credentialDatabase.get(token, tokenPassword, (err, credential) => {
        expect(err).toBeFalsy();
        expect(credential).toEqual({target: 'http://localhost:8000', auth: {method: 'none'}});
        done();
      });
    });
  });

  it("doesn't let you add a malformed credential", (done) => {
    request.put({
      url: 'http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259',
      json: {target: 'http://localhost:8000'},
      headers: {'x-authproxy-token-password': tokenPassword},
    }, (error, response, body) => {
      expect(response.statusCode).toBe(400);
      expect(body).toEqual({
        message: 'Field is required',
        data: {
          fieldErrors: [
            {
              field: 'auth',
              code: 'required',
              message: 'Field is required'
            }
          ]
        }
      });
      credentialDatabase.get(token, tokenPassword, (err, credential) => {
        expect(err).toBeFalsy();
        let whatItWasBefore = {target: 'http://localhost:8000', auth: {method: 'none'}};
        expect(credential).toEqual(whatItWasBefore);
        done();
      });
    });
  });

  it("doesn't let you add a malformed credential", (done) => {
    request.put({
      url: 'http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259',
      headers: {'x-authproxy-token-password': tokenPassword},
      json: {target: 'http://localhost:8000', auth: {method: 'illegal value'}}
    }, (error, response, body) => {
      expect(response.statusCode).toBe(400);
      credentialDatabase.get(token, tokenPassword, (err, credential) => {
        expect(err).toBeFalsy();
        let whatItWasBefore = {target: 'http://localhost:8000', auth: {method: 'none'}};
        expect(credential).toEqual(whatItWasBefore);
        done();
      });
    });
  });

  it("will tell you when a credential does exist", (done) => {
    request.head('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      expect(response.statusCode).toBe(200);
      done();
    });
  });

  it("knows the difference credential API and proxying '/'", (done) => {
    request.delete({
      url: 'http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259/',
      headers: {'x-authproxy-token-password': tokenPassword},
    }, (error, response, body) => {
      expect(response.statusCode).toBe(404);
      request.head('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
        expect(response.statusCode).toBe(200);
        done();
      });
    });
  });

  it("lets you delete a credential", (done) => {
    request.delete('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      expect(response.statusCode).toBe(200);
      request.head('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
        expect(response.statusCode).toBe(404);
        done();
      });
    });
  });

  afterAll((done) => {
    request.delete('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      done();
    });
  });
});
