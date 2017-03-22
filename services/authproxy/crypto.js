// borrowed some code from http://lollyrock.com/articles/nodejs-encryption/
var deasync = require('deasync');
var read = deasync(require('read'));

var CryptoJS = require("crypto-js");

let promptSecretKey = () => {
  return read({prompt: "Secret Key? ", silent: true});
};

class Crypto {
  constructor(secret) {
    this.secret = secret;
  }

  promptSecret() {
    this.secret = promptSecretKey();
    return this;
  }

  assertSecret() {
    if (!this.secret) {
      throw new Error('Crypto must be used only after setting a secret password');
    }
  }

  encrypt(text) {
    this.assertSecret();
    return CryptoJS.AES.encrypt(text, this.secret).toString();
  }

  decrypt(text) {
    this.assertSecret();
    return CryptoJS.AES.decrypt(text, this.secret).toString(CryptoJS.enc.Utf8);
  };
}
exports.Crypto = Crypto;
