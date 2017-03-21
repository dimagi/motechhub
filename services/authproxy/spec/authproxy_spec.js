/*globals describe, it, expect, beforeAll, afterAll */
let Crypto = require('../crypto.js').Crypto;
let CredentialDatabase = require('../credential-database.js').CredentialDatabase;
let AuthProxy = require('../authproxy.js').AuthProxy;
let DummyServer = require('../dummyserver.js').DummyServer;
let request = require('request');


describe("Auth Proxy's ability to proxy", () => {
  let authProxy, dummyServer, token, credentialDatabase;

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
    credentialDatabase.set(token, {target: 'http://localhost:9000', username: 'admin', password: '123'}, () => {
      done();
    });
  });

  afterAll(() => {
    authProxy.stop();
    dummyServer.stop();
  });

  it("lets you proxy GET using basic auth", (done) => {
    request.get('http://localhost:8000/c7de095ee07e4e1be55594d6d2ba4676/hello', function(error, response, body) {
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
    request.post('http://localhost:8000/c7de095ee07e4e1be55594d6d2ba4676/hello', function(error, response, body) {
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
    request.put('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      expect(response.statusCode).toBe(200);
      credentialDatabase.get(token, (err, credential) => {
        expect(err).toBeFalsy();
        expect(credential).toEqual({target: 'http://localhost:8000'});
        done();
      });
    }).json({target: 'http://localhost:8000'});
  });

  it("will tell you when a credential does exist", (done) => {
    request.head('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259', (error, response, body) => {
      expect(response.statusCode).toBe(200);
      done();
    });
  });

  it("knows the difference credential API and proxying '/'", (done) => {
    request.delete('http://localhost:8000/4dfdd3ab2d5a6be04b498dd27cba5259/', (error, response, body) => {
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
