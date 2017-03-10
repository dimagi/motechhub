let URL = 'http://localhost:7001';

let frisby = require('frisby');

function create(name) {
    return frisby.create(name)
        .expectHeaderContains('content-type', 'application/json');
}

create('(Clear from last run)').delete(URL + '/teststream');



create('Get list of streams')
  .get(URL + '/')
  .expectStatus(200)
  .expectJSON({
    'streams': []
  })
.toss();

create('GET nonexistent stream')
  .get(URL + '/teststream')
  .expectStatus(404)
  .expectJSON({
    'error': 'not_found',
    'reason': 'The stream does not exist.'
  })
.toss();

create('PUT new stream')
  .put(URL + '/teststream')
  .expectStatus(201)
  .expectJSON({
    'ok': true
  })
.toss();

create('GET existing stream')
  .get(URL + '/teststream')
  .expectStatus(200)
  .expectJSON({
    'name': 'teststream'
  })
.toss();

// put the same stream again, it'll give an error message
create('PUT same stream again')
  .put(URL + '/teststream')
  .expectStatus(412)
  .expectJSON({
    'error': 'file_exists',
    'reason': 'The stream could not be created, the file already exists.'
  })
.toss();

create('DELETE existing stream')
  .delete(URL + '/teststream')
  .expectStatus(200)
  .expectJSON({
    'ok': true
  })
.toss();

create('DELETE nonexistent stream')
  .delete(URL + '/teststream')
  .expectStatus(404)
  .expectJSON({
    'error': 'not_found',
    'reason': 'The stream does not exist.'
  })
.toss();
