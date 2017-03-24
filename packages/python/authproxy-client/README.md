authproxy-client: the python client for the authproxy server (services/authproxy)

# Installation

To install in your virtualenv, use:

```
pip install -e $MOTECHHUB/packages/python/authproxy-client
```

or simply include

```
-e $MOTECHHUB/packages/python/authproxy-client
```

in `requirements.txt`. You will need to replace `$MOTECHHUB`
with the actual relative path to the motechhub repo.


# Usage

Use the `AuthProxyClient` class to create a client object with your settings.
You will need to specify the authproxy's url, as well as a function to look up
a token password given the token. This will typically be stored in a database.

## Configure

```python
authproxy_client = AuthProxyClient(server_url='http://localhost:8000', get_password=get_token_password)
```


## Store credentials in authproxy

You can then send credentials to the authproxy.

```python
authproxy_client.create_or_update_credential(
    token,
    target='https://www.commcarehq.org/',
    auth=BasicAuth(
        username='admin',
        password='123',
    )
)
```

You should do this immediately after the user has entered them,
after which you should discard at least the password.
(It may make sense for you to keep a record of non-sensitive data such as the
target and the username so that you can display it later to the user, etc.)


## Make requests through authproxy

To make requests proxied through authproxy for a particular token, you ask for a special
"`requests`" object that behaves just like the popular python `requests` library.

```python
requests = self.authproxy_client.requests(self.token)

response = requests.get('/hello/world', auth=('admin', '123'))

if response.status_code == 200:
    result = response.json()
```

Note that since authproxy already stores the destination
and authentication keys associated with a token
(encrypted with a combination of an in-memory key
and the token password that `authproxy_client` automatically provides on each request),
you should specify just the path component of the uri,
beginning with a slash.
