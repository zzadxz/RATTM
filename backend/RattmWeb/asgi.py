"""
ASGI config for RattmWeb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/

----------------------------------------------------------------------------------
-> ASGI (Asynchronous Server Gateway Interface) specifies how the web server
communicates with the backend. 
-> Asynchronous allows servers to handle multiple requests at the same time.
-> The ASGI callable is application in this case, used by ASGI servers to handle 
incoming requests and returning responses.
-> Note: we can put "async" keyword infront of functions to define them as 
asynchronous functions.
----------------------------------------------------------------------------------
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RattmWeb.settings')

application = get_asgi_application() # The ASGI callable
