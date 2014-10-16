import os
import jinja2


DEBUG = True

SECRET_KEY = 'asdfjasdflkjsfewi23kjl3kjl45kjl56jk6hjb7lou0796kgfsa'

CONFIG = {
}


SRC_ROOT = os.path.dirname(os.path.realpath(__file__))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(SRC_ROOT),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://console.developers.google.com/>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
