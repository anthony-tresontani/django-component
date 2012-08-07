import copy

from django import template
from django.conf import settings
from django.core import exceptions, urlresolvers
from django.core.handlers.base import BaseHandler
from django.test import TestCase
from django.test.client import RequestFactory


def do_render_component(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return ComponentNode()


class ComponentNode(template.Node):
    def render(self, context):
        request = context['request']
        new_request = copy.copy(request)
        new_request.path_info = u'/component'

        handler = BaseHandler()
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
        callback, callback_args, callback_kwargs = resolver.resolve(new_request.path_info)
        response = callback(new_request, *callback_args, **callback_kwargs)
        if hasattr(response, 'render') and callable(response.render):
            response = response.render()
        
        return response.content

register = template.Library()
register.tag('render_component', do_render_component)
