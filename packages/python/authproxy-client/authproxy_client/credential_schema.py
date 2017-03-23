import jsonobject


class Credential(jsonobject.JsonObject):
    target = jsonobject.StringProperty(required=True)
    auth = jsonobject.ObjectProperty(lambda: Auth)


class Auth(jsonobject.JsonObject):
    method = jsonobject.StringProperty(required=True, validators=lambda value: value in _auth_methods)

    @classmethod
    def wrap(cls, obj):
        if cls is Auth:
            method = obj['method']
            try:
                subclass = _auth_methods[method]
            except KeyError:
                raise ValueError('auth method must be one of {}'.format(_auth_methods.keys()))
            else:
                return subclass.wrap(obj)
        else:
            return super(Auth, cls).wrap(obj)


class NoneAuth(Auth):
    method = 'none'


class BasicAuth(Auth):
    method = 'basic'
    username = jsonobject.StringProperty(required=True)
    password = jsonobject.StringProperty(required=True)


class ApiKeyAuth(Auth):
    method = 'apikey'
    username = jsonobject.StringProperty(required=True)
    apikey = jsonobject.StringProperty(required=True)


_auth_methods = {
    'none': NoneAuth,
    'basic': BasicAuth,
    'apikey': ApiKeyAuth,
}

# make sure the method property is consistent with the key in _auth_methods
assert [auth_class.method == method for method, auth_class in _auth_methods.items()]
