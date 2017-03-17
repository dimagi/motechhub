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
  .afterJSON((json) => {
    expect(json.length).toBe(2);
    // they will appear in reverse order from how they were sent
    let message1 = json[0];
    let message2 = json[1];
    expect(message1.created).toMatch(/^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d\d\d\dZ$/);
    expect(message1.body).toEqual({
      type: 'Character',
      name: 'Popeye',
      favoriteFood: 'Spinach',
    });

    expect(message2.created).toMatch(/^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d\d\d\dZ$/);
    expect(message2.body).toEqual({
      type: 'Character',
      name: 'Homer',
      favoriteFood: 'Donut',
    });

  })
  .toss();

create('Tear down stream')
  .delete(URL + '/testmessagestream').toss();
