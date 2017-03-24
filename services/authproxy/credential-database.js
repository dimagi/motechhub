let nano = require('nano');
let credentialSchema = require('./credential.js').credentialSchema;
let deasync = require('deasync');

function getDocId(token) {
  return `Token:${token}`;
}

class CredentialDatabase {
  constructor({dbUri, dbName, crypto}) {
    this.dbUri = dbUri;
    this.dbName = dbName;
    this.couch = nano(this.dbUri);
    this.db = this.couch.use(dbName);
    this.crypto = crypto;
  }

  init() {
    try {
      deasync(this.couch.db.create)(this.dbName);
    } catch (e) {
      if (e.statusCode === 412 && e.error === 'file_exists') {

      } else {
        throw e;
      }
    }
    console.log(`Created db ${this.dbName}`);
    let checksum = this.crypto.generateHash();
    try {
      deasync(this.db.insert)({_id: 'Checksum', checksum: checksum});
    } catch (e) {
      if (e.statusCode !== 409) {
        throw e;
      }
    }
    return this;
  }

  checkChecksum() {
    let checksum = deasync(this.db.get)('Checksum').checksum;
    return this.crypto.verifyHash(checksum);
  }

  set(token, tokenPassword, credentials, callback) {
    try {
      credentialSchema.validate(credentials);
    } catch (e) {
      callback(e);
      return;
    }

    let encryptedCredentials = this.crypto.encrypt(tokenPassword, JSON.stringify(credentials));
    this.db.get(getDocId(token), (err, body) => {
      if (err && err.statusCode === 404) {
        body = {_id: getDocId(token)};
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
    this.db.get(getDocId(token), (err, body) => {
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

  get(token, tokenPassword, callback) {
    this.db.get(getDocId(token), (err, body) => {
      if (!err) {
        let credentials;
        try {
          credentials = JSON.parse(this.crypto.decrypt(tokenPassword, body.credentials));
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
    this.db.head(getDocId(token), (err, body) => {
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
