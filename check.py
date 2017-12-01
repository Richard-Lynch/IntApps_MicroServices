#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)


def reqs(reqs):
    def wrap(f):
        def wrapped_f(self, **args):
            # ensure the requirements are met
            if all(req in args for req in reqs):
                # filter un-required keywords
                kwargs = {req: args[req] for req in reqs}
                # call func
                return f(self, **kwargs)
            else:
                raise my_errors.bad_request

        return wrapped_f

    return wrap
