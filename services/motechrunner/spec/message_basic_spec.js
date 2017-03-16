let URL = require('./constants.js').URL;
let create = require('./constants.js').create;
let messageId;

create('Initialize stream')
  .put(URL + '/testmessagestream').toss();


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
  .afterJSON((json) => {
    expect(json.length).toBe(1);
    json.forEach((message) => {
        expect(message.created).toMatch(/^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d\d\d\dZ$/);
        expect(message.body).toEqual({
          type: 'Character',
          name: 'Homer',
          favoriteFood: 'Donut',
        });
    });
  })
  .toss();

create('Tear down stream')
  .delete(URL + '/testmessagestream').toss();
