let URL = require('./constants.js').URL;
let create = require('./constants.js').create;

create('Initialize stream')
  .put(URL + '/testjobstream').toss();


create('Create job 1')
  .put(URL + '/testjobstream/job/556cfe1b-a4d5-4e39-b72e-60bb419975d4', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {}
    })
  })
  .expectStatus(201)
  .toss();

create('Create job 2')
  .put(URL + '/testjobstream/job/6b5a7000-704c-4557-bcac-fcf7d3f2d383', null, {
    body: JSON.stringify({
      javascript: '(function (message) {})',
      filter: {}
    })
  })
  .expectStatus(201)
  .toss();

create('Update job 2')
  .put(URL + '/testjobstream/job/6b5a7000-704c-4557-bcac-fcf7d3f2d383', null, {
    body: JSON.stringify({
      rev: 1,
      javascript: '(function (message) {})',
      filter: {}
    })
  })
  .expectStatus(201)
  .toss();


create('Get job list')
  .get(URL + '/testjobstream/job')
  .expectStatus(200)
  .expectJSON([{
    id: '556cfe1b-a4d5-4e39-b72e-60bb419975d4',
    rev: 1,
    javascript: '(function (message) {})',
    filter: {}
  }, {
    id: '6b5a7000-704c-4557-bcac-fcf7d3f2d383',
    rev: 2,
    javascript: '(function (message) {})',
    filter: {}
  }])
  .toss();

create('Tear down stream')
  .delete(URL + '/testjobstream').toss();
