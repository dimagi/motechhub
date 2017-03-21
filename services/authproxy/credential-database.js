let nano = require('nano');
let credentialSchema = require('./credential.js').credentialSchema;

class CredentialDatabase {
  constructor({dbUri, dbName, crypto}) {
    this.dbUri = dbUri;
    this.dbName = dbName;
    this.couch = nano(this.dbUri);
    this.db = this.couch.use(dbName);
    this.crypto = crypto;
  }

  init() {
    this.couch.db.create(this.dbName);
    console.log(`Created db ${this.dbName}`);
  }

  set(token, credentials, callback) {
    try {
      credentialSchema.validate(credentials);
    } catch (e) {
      callback(e);
      return;
    }

    let encryptedCredentials = this.crypto.encrypt(JSON.stringify(credentials));
    this.db.get(token, (err, body) => {
      if (err && err.statusCode === 404) {
        body = {_id: token};
      } else if (err) {
        callback(err);
        return;
      }
      body.credentials = encryptedCredentials;
      this.db.insert(body, (err, body) => {
        callback(err);
      });
    });
  }

  clear(token, callback) {
    this.db.get(token, (err, body) => {
      if (err && err.statusCode === 404) {
        // already doesn't exist? no problem!
        callback();
      } else if (err) {
        callback(err);
      } else {
        this.db.destroy(body._id, body._rev, (err, body) => {
          callback(err);
        });
      }
    });
  }

  get(token, callback) {
    this.db.get(token, (err, body) => {
      if (!err) {
        let credentials;
        try {
          credentials = JSON.parse(this.crypto.decrypt(body.credentials));
        } catch (e) {
          callback({"name": "Decryption Error", "message": "Could not retrieve the encrypted message"});
          return
        }
        callback(undefined, credentials);
      } else {
        callback(err);
      }
    })
  }

  has(token, callback) {
    this.db.head(token, (err, body) => {
      if (!err) {
        callback(undefined, true);
      } else if (err.statusCode === 404) {
        callback(undefined, false)
      } else {
        callback(err);
      }
    });
  }

}

exports.CredentialDatabase = CredentialDatabase;
