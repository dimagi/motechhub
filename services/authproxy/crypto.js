// borrowed some code from http://lollyrock.com/articles/nodejs-encryption/
var prompt = require('syncprompt');
var CryptoJS = require("crypto-js");

let promptSecretKey = () => {
  let secret = prompt("Secret Key? ", { secure: true });
  console.log();
  return secret;
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
