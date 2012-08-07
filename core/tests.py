import copy

from django.test import TestCase
from django.core.handlers.base import BaseHandler
from django.core import exceptions, urlresolvers
from django.conf import settings
from django.test.client import RequestFactory




class SimpleTest(TestCase):
    def test_resolve_request(self):
        self.factory = RequestFactory()
        request = self.factory.get('/home')
        new_request = copy.copy(request)

        handler = BaseHandler()
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
        callback, callback_args, callback_kwargs = resolver.resolve(new_request.path_info)
        response = callback(new_request, *callback_args, **callback_kwargs)
        if hasattr(response, 'render') and callable(response.render):
            response = response.render()
        self.assertIsNotNone(response.content)
