/*globals describe, it, expect, beforeAll, afterAll */
let Crypto = require('../crypto.js').Crypto;
let CredentialDatabase = require('../credential-database.js').CredentialDatabase;

describe("Credential Database", () => {
  let credentialDatabase = new CredentialDatabase({
    dbUri: 'http://localhost:5984',
    dbName: 'test_authproxy',
    crypto: new Crypto('*** secret password ***'),
  });
  let credential = {target: 'example.com', auth: {method: 'basic', username: 'admin', password: '123'}};

  credentialDatabase.init();
  let token = 'd3b07384d113edec49eaa6238ad5ff00';

  it("can store things", (done) => {
    credentialDatabase.set(token, credential, (err) => {
      expect(err).toEqual(null);
      done();
    });
  });

  it("can retrieve things", (done) => {
    credentialDatabase.get(token, (err, credentials) => {
      expect(err).toEqual(undefined);
      expect(credentials).toEqual(credential);
      done();
    });
  });

  it("will error when the credential not found", (done) => {
    credentialDatabase.get('nonexistentdoc', (err) => {
      expect(err).toBeTruthy();
      done();
    })
  });

  it("stores the credential encrypted in the database", (done) => {
    credentialDatabase.db.get(`Token:${token}`, (err, body) => {
      expect(err).toBeFalsy();
      // AES output always starts with 'Salted__' in base64, or 'U2FsdGVkX1'
      expect(body.credentials.slice(0, 10)).toEqual('U2FsdGVkX1');
      done();
    })
  });

  it("lets you see if something is stored yet", (done) => {
    credentialDatabase.has(token, (err, hasToken) => {
      expect(err).toBeFalsy();
      expect(hasToken).toBeTruthy();
      credentialDatabase.has('notthere', (err, hasToken) => {
        expect(err).toBeFalsy();
        expect(hasToken).toBeFalsy();
        done();
      });
    });
  });

  it("lets you delete credentials", (done) => {
    credentialDatabase.clear(token, (err) => {
      expect(err).toBeFalsy();
      credentialDatabase.has(token, (err, hasToken) => {
        expect(hasToken).toBeFalsy();
        done();
      });
    })
  });
});
