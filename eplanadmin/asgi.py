import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import api.routing  # Import the routing file where WebSocket routes are defined

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eplanadmin.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns  # Pointing to your WebSocket routes
        )
    ),
})

