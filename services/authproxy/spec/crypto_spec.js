/*globals describe, it, expect, beforeAll, afterAll */
let Crypto = require('../crypto.js').Crypto;

describe('Crypto', () => {
  it('lets you pass in a secret', () => {
    let crypto = new Crypto('*** my password ***');
    expect(crypto.secret).toEqual('*** my password ***');
  });

  it("doesn't let you encrypt without a secret", () => {
    let crypto = new Crypto();
    expect(() => crypto.encrypt('tokenPa$$word', 'plaintext')).toThrow(
      new Error('Crypto must be used only after setting a secret password'));
  });

  it("encrypts the same string differently every time", () => {
    let crypto = new Crypto('****');
    expect(crypto.encrypt('tokenPa$$word', 'mytext')).not.toEqual(
           crypto.encrypt('tokenPa$$word', 'mytext'));
  });

  it("returns output that starts like you would expect AES to", () => {
    let crypto = new Crypto('****');
    expect(crypto.encrypt('tokenPa$$word', 'some text').slice(0, 10)).toEqual('U2FsdGVkX1');
  });

  it("lets you get back the original", () => {
    let crypto = new Crypto('****');
    let cypherText = crypto.encrypt('tokenPa$$word', 'some text');
    let plainText = crypto.decrypt('tokenPa$$word', cypherText);
    expect(plainText).toEqual('some text');
  });
});
