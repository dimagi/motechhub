let URL = require('./constants.js').URL;
let create = require('./constants.js').create;

create('Initialize stream')
  .put(URL + '/testjobstream').toss();


create('Get nonexistent job')
  .get(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4')
  .expectStatus(404)
  .expectJSON({
    'error': 'not_found',
    'reason': 'The job does not exist.'
  }).toss();


create('Create job')
  .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {}
    })
  })
  .expectStatus(201)
  .expectJSON({
    ok: true,
    rev: 1,
    id: '556cfe1b-a4d5-4e39-b72e-60bb419975d4'
  })
  .toss();

create('GET job')
  .get(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4')
  .expectStatus(200)
  .expectJSON({
    id: '556cfe1b-a4d5-4e39-b72e-60bb419975d4',
    rev: 1,
    javascript: '(function (message) {})',
    filter: {}
  })
  .toss();

create('Update job')
  .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {},
      rev: 1
    })
  })
  .expectStatus(201)
  .expectJSON({
    ok: true,
    rev: 2,
    id: '556cfe1b-a4d5-4e39-b72e-60bb419975d4'
  })
  .toss();

create('Updating with old rev causes a Conflict')
  .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {},
      rev: 1
    })
  })
  .expectStatus(409)
  .expectJSON({
    error: 'conflict',
    reason: 'The rev must match the rev of the last update to this job.',
  })
  .toss();

create('Updating with future rev causes a Conflict')
  .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {},
      rev: 3
    })
  })
  .expectStatus(409)
  .expectJSON({
    error: 'conflict',
    reason: 'The rev must match the rev of the last update to this job.',
  })
  .toss();

[{
    // testing this typo
    js: '(function (message) {})',
    filter: {},
    rev: 2
  }, {
  }, {
    javascript: '(function (message) {})',
    filter: '',
    rev: 2
}].forEach(function (body) {
  create('Creating a job without adhering to the spec causes a Bad Request')
    .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
      body: JSON.stringify(body)
    })
    .expectStatus(400)
    .expectJSON({
      error: 'bad_request',
      reason: 'Request body JSON must adhere to spec',
    })
    .toss();
});

create('Creating a job with bad javascript causes a Bad Request')
.put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
  body: JSON.stringify({
    javascript: '(function (message)',
    filter: {},
    rev: 2
  })
})
.expectStatus(400)
.expectJSON({
  error: 'bad_request',
  reason: 'Javascript must be valid.',
})
.toss();

create('Tear down stream')
  .delete(URL + '/testjobstream').toss();
