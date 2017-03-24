AuthProxy is a credential store and HTTP proxy
that can make requests on your behalf without you or it persisting all of the information
an attacker would need to make the request.


# Here's how it works

- A user tells you their credentials
- You create a token and a password for the credentials
- You post the credentials with the token and password to AuthProxy
- AuthProxy encrypts the credentials with a combination of the password you supply and an in-memory secret key
- AuthProxy stores the encrypted credential indexed by token, and discards the token password
- You store the token and token-password for later retrieval, and discard the user's credentials

At this point neither you nor AuthProxy alone have enough information to reconstruct the user's credentials.
You will also never see the credentials again once you discard them:
instead, you will make all request that you make on the user's behalf through AuthProxy,
using the token and token-password.

When you want to make a request on behalf of the user:

- make the exact request you'd make, but to AuthProxy at `/<token>/<uri>` instead of
  to the external service at `/<uri>`.
- include the `X-AuthProxy-Token-Password` header
- AuthProxy will then reconstruct the credentials in memory, make the request,
  and send you the response.

# Set up (dev)

You will need couchdb installed.
By default this will create a db named 'authproxy' (and 'test_authproxy' for tests).

```
cd authtest
npm install
bash maketestcert.sh  # makes localhost.{key,cert}
cp localsettings.yml.example localsettings.yml
node manage.js syncdb
```

Syncdb will prompt you for a that will be used as the in-memory secret.
You must enter this same password every time you start the server.

To run the server

```
node manage.js runserver
```

to test

```
jasmine
```

# API

## Add or update credential

```
PUT /<token>
X-AuthProxy-Token-Password: <password>

{
  "target": <url>,
  "auth": {
    "method": "basic",
    "username": <username>
    "password": <password>
  }
}
```

- `201` Means success
- `400` Means there is a problem with your request. The most common issues are
  - `X-AuthProxy-Token-Password` header is missing or empty
  - the credential does not adhere to the expected schema

## Check whether a credential exists

```
HEAD /<token>
```

- `200` Means it exists
- `404` Means it does not

## Remove a credential

```
DELETE /<token>
```


## Proxy a request

Make any request

```
<any method> /<token>/<uri>
...
X-AuthProxy-Token-Password: <password>

...
```


# Supported Auth Methods

While Basic auth may be the most common, other methods are supported. Currently,
the methods supported are:

## None

{
    "method": "none"
}

## Basic

```
{
    "method": "basic",
    "username": <username>
    "password": <password>
}
```

## ApiKey

{
    "method": "apikey",
    "username": <username>
    "apikey": <apikey>
}
