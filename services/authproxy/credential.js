let commonSchema = require('common-schema');

function matchStringValue(requiredValue) {
  return {
    type: String,
    validate: (value) => {
      if (value !== requiredValue) {
        throw new commonSchema.FieldError('invalid', `Value must be '${requiredValue}'`);
      }
    }
  };
}

let credentialSchema = commonSchema.createSchema({
  target: String,
  auth: commonSchema.or({required: true}, {
    method: matchStringValue('none'),
  }, {
    method: matchStringValue('basic'),
    username: String,
    password: String,
  }, {
    method: matchStringValue('apikey'),
    username: String,
    apikey: String,
  })
});


exports.credentialSchema = credentialSchema;
