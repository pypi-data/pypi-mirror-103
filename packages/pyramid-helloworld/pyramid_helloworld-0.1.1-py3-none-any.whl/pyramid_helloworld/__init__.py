import pkg_resources

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.router import Router

__version__ = pkg_resources.get_distribution("pyramid-helloworld").version


def hello_world(request):
    return Response("Hello World!")


def main(global_config: dict, **settings) -> Router:
    """Build the pyramid WSGI App."""

    with Configurator(settings=settings) as config:
        config.add_route("root", "/")
        config.add_view(hello_world, route_name="root")
        app = config.make_wsgi_app()
        return app
