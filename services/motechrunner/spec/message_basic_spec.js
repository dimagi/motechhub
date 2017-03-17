let URL = require('./constants.js').URL;
let create = require('./constants.js').create;
let messageId;
let datetimeRegex = /^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d\d\d\dZ$/;


create('Initialize stream')
  .put(URL + '/testmessagestream').toss();


create('Job to match a message')
  .put(URL + '/testmessagestream/job/1b7e31c1-7a23-438e-b1e5-2737eaf70055', null, {
    body: JSON.stringify({
        filter: {},  // match all
        javascript: '(function (message) {})',
    })
  })
  .expectStatus(201)
  .toss();

create('Post message')
  .post(URL + '/testmessagestream/message', null, {
    body: JSON.stringify({
      type: 'Character',
      name: 'Homer',
      favoriteFood: 'Donut',
    })
  })
  .expectStatus(201)
  .expectJSON({
    ok: true
  }).expectJSONTypes({
    id: 'String'
  }).afterJSON((json) => {
    messageId = json.id;
  })
  .toss();

create('Post second message')
  .post(URL + '/testmessagestream/message', null, {
    body: JSON.stringify({
      type: 'Character',
      name: 'Popeye',
      favoriteFood: 'Spinach',
    })
  })
  .expectStatus(201)
  .expectJSON({
    ok: true
  }).expectJSONTypes({
    id: 'String'
  }).afterJSON((json) => {
    messageId = json.id;
  })
  .toss();

create('Get messages without limit fails')
  .get(URL + '/testmessagestream/message')
  .expectStatus(400)
  .expectJSON({
    error: 'bad_request',
    reason: 'The limit GET param is required and must be an integer.',
  })
  .toss();

create('Get messages')
  .get(URL + '/testmessagestream/message?limit=10')
  .expectStatus(200)
  .expectJSONTypes('*', {
    created: function (val) {expect(val).toMatch(datetimeRegex)},
    body: {},
    runs: [{
      created: function (val) {expect(val).toMatch(datetimeRegex)},
      runJobs: function (val) {
        expect(val).toEqual([{
          job: {id: '1b7e31c1-7a23-438e-b1e5-2737eaf70055', rev: 1},
          state: 'scheduled',
        }]);
      }
    }]
  })
  .afterJSON((json) => {
    expect(json.length).toBe(2);
    // they will appear in reverse order from how they were sent
    let message1 = json[0];
    let message2 = json[1];
    expect(message1.body).toEqual({
      type: 'Character',
      name: 'Popeye',
      favoriteFood: 'Spinach',
    });
    expect(message1.runs.length).toBe(1);

    expect(message2.body).toEqual({
      type: 'Character',
      name: 'Homer',
      favoriteFood: 'Donut',
    });
    expect(message2.runs.length).toBe(1);
  })
  .toss();

create('Tear down stream')
  .delete(URL + '/testmessagestream').toss();
