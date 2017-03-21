/*globals describe, it, expect, beforeAll, afterAll */
let credentialSchema = require('../credential.js').credentialSchema;
let commonSchema = require('common-schema');

describe('Credential Schema', () => {
  it('accepts no auth', () => {
    credentialSchema.validate({
      target: 'example.com',
      auth: {
        method: 'none',
      }
    });
  });

  it('accepts basic auth', () => {
    credentialSchema.validate({
      target: 'example.com',
      auth: {
        method: 'basic',
        username: 'marvin',
        password: '******',
      }
    });
  });

  it('accepts apikey auth', () => {
    credentialSchema.validate({
      target: 'example.com',
      auth: {
        method: 'apikey',
        username: 'marvin',
        apikey: '********',
      }
    });
  });
  it('rejects missing auth', () => {
    expect(() => {
      credentialSchema.validate({
        target: 'example.com',
      });
    }).toThrowError(commonSchema.ValidationError);
  });
  it('rejects unknown auth method', () => {
    expect(() => {
      credentialSchema.validate({
        target: 'example.com',
        auth: {
          method: 'not a real method'
        }
      });
    }).toThrowError(commonSchema.ValidationError);
  });
});
