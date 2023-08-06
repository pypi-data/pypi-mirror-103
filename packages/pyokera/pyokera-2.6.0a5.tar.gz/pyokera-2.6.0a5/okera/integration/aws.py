import logging
import requests
import errno
import os

# Boto3 and its dependencies are not an explicit pyokera
# dependency, so we try and import and note if we fail
boto_imported = False
try:
    from okera.integration import boto as okera_boto
    boto_imported = True
except Exception:
    pass

from okera.integration import boto as okera_boto
from okera.integration.boto import OkeraException

LOG = logging.getLogger(__name__)

_VALID_COMMANDS = ['s3', 's3api']
_CONFIG_KEY_OKERA = 'okera'
_CONFIG_KEY_REST = 'rest'
_CONFIG_KEY_PROXY = 'proxy'
_CONFIG_KEY_SOURCE = 'token_source'
_CONFIG_KEY_TOKEN = 'token'
_AUTH_SERVER_URI= "http://localhost:5001"

def _get_info_from_profile(profile):
    proxy_endpoint = None
    rest_endpoint = None
    token = None

    if _CONFIG_KEY_OKERA not in profile:
        return None

    info = profile[_CONFIG_KEY_OKERA]
    if _CONFIG_KEY_PROXY not in info \
        or _CONFIG_KEY_REST not in info \
        or ( _CONFIG_KEY_TOKEN not in info \
        or _CONFIG_KEY_SOURCE not in info ):
        return None

    proxy_endpoint = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_PROXY]
    rest_endpoint = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_REST]
    token_source = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_SOURCE]
    token = profile[_CONFIG_KEY_OKERA][_CONFIG_KEY_TOKEN]

    return proxy_endpoint, rest_endpoint, token, token_source

def _register_okera_proxy(parsed_args, **kwargs):
    if parsed_args.debug:
        LOG.setLevel(logging.DEBUG)

    if not parsed_args.command:
        LOG.debug("No command")
        return

    command = parsed_args.command.lower()
    if command not in _VALID_COMMANDS:
        LOG.debug("Not valid command: %s" % command)
        return

    if 'session' not in kwargs or not kwargs['session']:
        LOG.debug("No session")
        return

    session = kwargs['session']
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)

    okera_info = _get_info_from_profile(session.get_scoped_config())
    if not okera_info:
        LOG.debug("No Okera configuration found")
        return

    LOG.debug("Injecting Okera proxy")
    proxy, rest, token, token_source = okera_info


    user = os.getenv('USER')
    if not user:
      raise OkeraException("The USER environment variable is not defined.")
    okera_session = okera_boto.okera_session(session, user, token, token_source, rest, proxy)
    kwargs['session'] = okera_session

    # TODO: rather than setting this, we should automatically
    # retrieve the CA bundle from the server and set it so we
    # still validate it.
    parsed_args.verify_ssl = False

def awscli_initialize(cli):
    if not boto_imported:
        raise Exception("okera boto integration could not be imported")

    cli.register('top-level-args-parsed', _register_okera_proxy)