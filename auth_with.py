#!/usr/local/bin/python3
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check


def credentials(f):
    """Decorator verifyinguser credentials(username and password)"""
    @check.reqs(['auth', 'message'])
    def wrapped_f(self, *args, **kwargs):
        auth = kwargs.get('auth')
        message = kwargs.get('message')
        user_data = self.verify_user(**auth)
        return auth['password'], f(self, user_data, *args, **message)

    return wrapped_f
