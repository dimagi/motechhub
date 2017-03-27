let authproxy = require('authproxy');


let credentialDatabase = new authproxy.CredentialDatabase({
  dbUri: 'http://localhost:5984',
  dbName: 'test_authproxy_client',
  crypto: new authproxy.Crypto('*** secret password ***'),
}).init();
new authproxy.AuthProxy({credentialDatabase}).listen();
new authproxy.DummyServer({port: 9000, username: 'admin', password: '123'}).listen();
