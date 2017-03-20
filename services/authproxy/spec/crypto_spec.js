let Crypto = require('../crypto.js').Crypto;

describe('Crypto', () => {
  it('lets you pass in a password', () => {
    let crypto = new Crypto('*** my password ***');
    expect(crypto.secret).toEqual('*** my password ***');
  });

  it("doesn't let you encrypt without a password", () => {
    let crypto = new Crypto();
    expect(() => crypto.encrypt('plaintext')).toThrow(
      new Error('Crypto must be used only after setting a secret password'));
  });

  it("encrypts the same string differently every time", () => {
    let crypto = new Crypto('****');
    expect(crypto.encrypt('mytext')).not.toEqual(crypto.encrypt('mytext'));
  });

  it("returns output that starts like you would expect AES to", () => {
    let crypto = new Crypto('****');
    expect(crypto.encrypt('some text').slice(0, 10)).toEqual('U2FsdGVkX1');
  });
});
