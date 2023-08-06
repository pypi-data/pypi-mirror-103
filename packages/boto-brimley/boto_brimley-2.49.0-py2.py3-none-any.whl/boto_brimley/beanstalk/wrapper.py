"""Wraps layer1 api methods and converts layer1 dict responses to objects."""
from boto_brimley.beanstalk.layer1 import Layer1
import boto_brimley.beanstalk.response
from boto_brimley.exception import BotoServerError
import boto_brimley.beanstalk.exception as exception


def beanstalk_wrapper(func, name):
    def _wrapped_low_level_api(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except BotoServerError as e:
            raise exception.simple(e)
        # Turn 'this_is_a_function_name' into 'ThisIsAFunctionNameResponse'.
        cls_name = ''.join([part.capitalize() for part in name.split('_')]) + 'Response'
        cls = getattr(botobrimley.beanstalk.response, cls_name)
        return cls(response)
    return _wrapped_low_level_api


class Layer1Wrapper(object):
    def __init__(self, *args, **kwargs):
        self.api = Layer1(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return beanstalk_wrapper(getattr(self.api, name), name)
        except AttributeError:
            raise AttributeError("%s has no attribute %r" % (self, name))
