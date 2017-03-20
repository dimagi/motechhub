let nano = require('nano');


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
  }

  set(token, credentials, callback) {
    let encryptedCredentials = this.crypto.encrypt(JSON.stringify(credentials));
    this.db.get(token, (err, body) => {
      if (err && err.statusCode === 404) {
        body = {_id: token};
      } else if (err) {
        callback(err);
      }
      body.credentials = encryptedCredentials;
      this.db.insert(body, (err, body) => {
        callback(err);
      });
    });
  }

  get(token, callback) {
    this.db.get(token, (err, body) => {
      if (!err) {
        let credentials = JSON.parse(this.crypto.decrypt(body.credentials));
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
