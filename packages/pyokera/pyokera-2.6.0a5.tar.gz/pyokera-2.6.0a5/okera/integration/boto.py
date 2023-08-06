# Copyright 2020 Okera Inc. All Rights Reserved.

import boto3
import botocore
import requests
from pathlib import Path
import os

from botocore.credentials import DeferredRefreshableCredentials, CredentialProvider

USERS_TOKEN_PATH = (os.getenv("HOME") + '/.okera')

class OkeraException(Exception):
    pass

class OkeraCredentialProvider(CredentialProvider):
    CANONICAL_NAME = "okera-aws-creds"

    def __init__(self, rest_api_url, user, token, token_source=config, verify_ssl=False):
        super().__init__()
        self._okera_rest_api_url = rest_api_url.rstrip('/')
        self._okera_token = _resolve_token(user, token, token_source)
        self._verify_ssl = verify_ssl

    def load(self):
        creds = DeferredRefreshableCredentials(refresh_using=self._refresh, method="sts-assume-role")
        return creds

    def _refresh(self):
        response = self._custom_aws_cred_refresh()
        credentials = {
            "access_key": response.get("key"),
            "secret_key": response.get("secret"),
            "expiry_time": response.get("expiry"),
            "token": None,
        }
        return credentials

    def _custom_aws_cred_refresh(self):
        api_url = "%s/%s" % (self._okera_rest_api_url, "api/v2/aws-tokens")
        headers = {"Authorization": "Bearer %s" % self._okera_token}
        res = requests.post(api_url, headers=headers, verify=self._verify_ssl)
        if res.status_code in (401, 403, 405):
            raise OkeraException("Error in authenticating credentials request: %s" % res.text)
        else:
            return res.json()

    def _read_token(token_file, user):
        try:
            with open(token_file, 'r') as file:
                data = file.read()
                return data
        except OSError as e:
            if (e.errno == errno.EACCES):
                raise OkeraException("No read access to %s's token file." % user, s)
            else:
                raise OkeraException("Error reading user's token file.", e)


    def _resolve_token(user, token, token_source):
        # token in home dir is priority, otherwise token_source
        home_token = Path(USERS_TOKEN_PATH)
        if home_token.is_file():
            return _read_token(home_token, user)
        elif ( "authserver" == token_source ):
            auth_uri=(_AUTH_SERVER_URI + "/" + user)
            res = requests.get(auth_uri)
            if res.status_code in (401, 403, 405):
                raise OkeraException("Error in retrieving user's JWT token: %s" % res.text)
            else:
                token_file = res.text
            data = _read_token(token_file, user)
            return data
        elif ( "config" == token_source ):
            return token

def okera_session(session, user, token, token_source, rest_uri, proxy_uri):
    bc_session = None
    if isinstance(session, botocore.session.Session):
        bc_session = session
    else:
        bc_session = session._session

    boto3_session = session

    # TODO: don't assume it's a cred resolver
    cred_chain = bc_session.get_component('credential_provider')
    okera_cred_provider = OkeraCredentialProvider(rest_uri, user, token, token_source)
    if cred_chain.providers:
        first_provider = cred_chain.providers[0].METHOD
        cred_chain.insert_before(first_provider, okera_cred_provider)
    else:
        cred_chain.providers.insert(0, okera_cred_provider)
    config = botocore.config.Config(
        proxies={'https': proxy_uri})

    orig_config = bc_session.get_default_client_config()
    if not orig_config:
        orig_config = botocore.config.Config()

    bc_session.set_default_client_config(orig_config.merge(config))

    return boto3_session