let frisby = require('frisby');

exports.URL = 'http://localhost:7001';

exports.create = function create(name) {
    return frisby.create(name)
        .expectHeaderContains('content-type', 'application/json');
};
