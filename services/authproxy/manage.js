let yaml = require('js-yaml');
let fs = require('fs');
let Crypto = require('./crypto.js').Crypto;
let CredentialDatabase = require('./credential-database.js').CredentialDatabase;
let AuthProxy = require('./authproxy.js').AuthProxy;
let request = require('request');

function runserver(localsettings) {
  let credentialDatabase = new CredentialDatabase({
    dbUri: localsettings.COUCHDB.uri,
    dbName: localsettings.COUCHDB.dbName,
    crypto: new Crypto().promptSecret(),
  });

  let verified = credentialDatabase.checkChecksum();

  if (verified) {
    new AuthProxy({
      credentialDatabase,
      ssl: {
        key: fs.readFileSync('localhost.key', 'utf8'),
        cert: fs.readFileSync('localhost.cert', 'utf8')
      }
    }).listen();
  } else {
    console.log('There was a problem with your password');
    process.exit(1);
  }


}

function syncdb(localsettings) {
  let credentialDatabase = new CredentialDatabase({
    dbUri: localsettings.COUCHDB.uri,
    dbName: localsettings.COUCHDB.dbName,
    crypto: new Crypto().promptSecret(),
  });
  credentialDatabase.init();
}

if (require.main == module) {
  let localsettings;
  try {
    fs.statSync('./localsettings.yml')
  } catch (e) {
    console.log("You are missing localsettings.yml. Try\n" +
      "  cp localsettings.yml.example localsettings.yml");
    process.exit(1);
  }
  try {
    localsettings = yaml.safeLoad(fs.readFileSync('./localsettings.yml', 'utf8'));
  } catch (e) {
    console.log("Error parsing localsettings.yml:\n", e);
    process.exit(1);
  }

  if (process.argv[2] == 'runserver') {
    runserver(localsettings);
  } else if (process.argv[2] == 'syncdb') {
    syncdb(localsettings);
  }
}
