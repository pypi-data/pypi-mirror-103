import abc
import base64
import hashlib
import secrets
import uuid
from urllib.parse import urlencode

import requests

from . import adapters, exceptions


class AbstractBasePKCEFlowManager(abc.ABC):
    authorization_path = "authorize/"
    client_id = None
    client_secret = None
    code_challenge_method = "S256"
    grant_type = "authorization_code"
    redirect_uri = None
    response_type = "code"
    root_url = None
    scope = None
    token_fetch_path = "token/"

    def __init__(self, *args, **kwargs):
        self._assert_attributes(
            ("client_id", "client_secret", "redirect_uri", "root_url", "scope")
        )

    def _assert_attributes(self, attributes):
        not_configured = [
            attribute for attribute in attributes if getattr(self, attribute) is None
        ]

        if len(not_configured) == 0:
            return

        raise exceptions.ImproperlyConfigured(
            "AbstractBasePKCEFlowManager requires that its subclasses "
            + "define the following attributes you haven't defined: "
            + ", ".join(not_configured)
        )

    def make_user_secrets(self, *, user):
        state = self.make_user_state(user=user)
        code_verifier = self.make_user_code_verifier(user=user)
        code_challenge = self.make_user_code_challenge(
            user=user, code_verifier=code_verifier
        )
        self.store_user_secrets(
            user=user,
            state=state,
            code_verifier=code_verifier,
            code_challenge=code_challenge,
        )
        return state, code_verifier, code_challenge

    def make_user_state(self, *, user):
        return str(uuid.uuid4())

    def make_user_code_verifier(self, *, user, nbytes=48):
        return secrets.token_urlsafe(nbytes)

    def make_user_code_challenge(self, *, user, code_verifier):
        return (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("ascii")).digest()
            )
            .decode("ascii")
            .rstrip("=")
        )

    def get_authorization_url(self, *, user, state=None, code_challenge=None):
        return (
            self.root_url
            + self.authorization_path
            + "?"
            + self.get_authorization_url_query_string(
                user=user, state=state, code_challenge=code_challenge
            )
        )

    def get_authorization_url_query_string(self, *, user, state, code_challenge):
        extra_query_params = self.get_authorization_url_extra_query_params()
        return urlencode(
            {
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "response_type": "code",
                "state": state or self.retrieve_user_state(user),
                "scope": "read_api",
                "code_challenge": code_challenge
                or self.retrieve_user_code_challenge(user),
                "code_challenge_method": "S256",
                **extra_query_params,
            }
        )

    def get_authorization_url_extra_query_params(self, **kwargs):
        return kwargs

    def fetch_access_token(self, *, user, state, code):
        if not self.check_user_state(user=user, state=state):
            raise exceptions.StateForgeryError

        with requests.Session() as session:
            session.mount(self.root_url, adapters.exponential_backoff_adapter)
            try:
                resp = session.post(
                    self.get_access_token_fetch_url(),
                    json=self.get_access_token_fetch_payload(user=user, code=code),
                    timeout=(5, 5),
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as exc:
                raise exceptions.PKCEFlowError(response=resp) from exc
            except requests.exceptions.RequestException as exc:
                raise exceptions.PKCEFlowError() from exc

        return resp

    def get_access_token_fetch_url(self):
        return self.root_url + self.token_fetch_path

    def get_access_token_fetch_payload(self, *, user, code):
        return {
            "code_verifier": self.retrieve_user_code_verifier(user),
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

    @abc.abstractmethod
    def store_user_secrets(self, *, user, state, code_verifier, code_challenge):
        pass

    @abc.abstractmethod
    def retrieve_user_state(self, user):
        pass

    @abc.abstractmethod
    def retrieve_user_code_challenge(self, user):
        pass

    @abc.abstractmethod
    def retrieve_user_code_verifier(self, user):
        pass

    @abc.abstractmethod
    def check_user_state(self, *, user, state):
        pass
