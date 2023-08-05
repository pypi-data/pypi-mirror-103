# PKCE-flow


PKCE-flow is a utility for obtaining access tokens using [the PKCE-enhanced authorization code flow (Oauth)](https://tools.ietf.org/html/rfc7636)


## Quick Start


### First Things First


We'll be walking through the creation of a utility for obtaining an access token that will allow us access GitLab resources on behalf of a particular user.

If you plan to _work through_ this, then you'll need to take five minutes (approx.) to create an Application with GitLab, so that you can have a client id and secret.

You can use any other service of your choice which implements PKCE OAuth. The process will be the same.


### Creating a PKCEFlowManager Instance


#### Subclass the Manager Class


```python
from pkce_flow import AbstractBasePKCEFlowManager


class GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):
    pass
```


#### Configure the Required Attributes


```python
from pkce_flow import AbstractBasePKCEFlowManager


class GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):
    client_id = 'our GitLab application id'
    client_secret = 'our GitLab application secret'
    redirect_uri = 'http://127.0.0.1:8000/oauth/gitlab/callback/'
    root_url = 'https://gitlab.com/oauth/'
    scope = 'read_api'
```

A quick description of the attributes we're defining:

* __client_id__: The ID of the developer application that will be requesting access to the resources on the user's behalf. The application must have been already created by the developer with the service.

* __client_secret__: The SECRET KEY of the developer application.

* __redirect_uri__: The redirect uri or callback uri that was specified by the developer when they created the developer application.

* __root_url__: The base url for authentication with the service.

* __scope__: Space delimited permission scopes.


#### Override the _Hook_ Methods


```python
from pkce_flow import AbstractBasePKCEFlowManager


class GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):
    client_id = 'our GitLab application id'
    client_secret = 'our GitLab application secret'
    redirect_uri = 'http://127.0.0.1:8000/oauth/gitlab/callback/'
    root_url = 'https://gitlab.com/oauth/'
    scope = 'read_api'

    def store_user_secrets(self, user, state, code_verifier, code_challenge):
        # write code to persist the state, code verifier, and code challenge
        # against the user in a place you can retrieve them later
        ...

    def retrieve_user_state(self, user):
        # write code to retrieve the state which was persisted against
        # the argument user
        ...
        return state

    def retrieve_user_code_challenge(self, user):
        # write code to retrieve the code challenge which was
        # persisted against the argument user
        ...
        return code_challenge

    def retrieve_user_code_verifier(self, user):
        # write code to retrieve the code verifier which was
        # persisted against the argument user
        ...
        return code_verifier

    def check_user_state(self, user, state):
        # write code to check whether argument state is the same as
        # the state that was persisted against the argument user
        ...
        return is_same
```


#### Instantiate a Project-wide Manager from Your Subclass


```python
gitlab_manager = GitLabPKCEFlowManager()
```


### Using the Manager Instance


So, a user of your web app wants to give you permission to access resources on GitLab on their behalf. And you've created a GitLab PKCE-flow manager for this.

The next thing to do is to make the secrets needed for the PKCE flow.

```python
state, verifier, challenge = gitlab_manager.make_user_secrets(user=user)
```

Since you've already _taught_ your manager how to store secrets against a user, it will store these secrets against the argument user before returning them to you.

After this, you get the url which you will send/redirect the user to, so they can authorize your request for an access token on their behalf.

```python
url = gitlab_manager.get_authorization_url(user=user)
```

Then in your web app, in the view which handles the endpoint corresponding to the redirect uri, you extract the `state` and `code` query parameters so you can fetch the user's access token with their values.

```python
from requests.exceptions import RequestException
from pkce_flow.exceptions import StateForgeryException


state = ...  # extract value of the query param 'state' from request
code = ...  # extract value of the query param 'code' from request

try:
    token_resp = gitlab_manager.fetch_access_token(
        user=user, state=state, code=code
    )
except StateForgeryException:
    ...
except RequestException:
    ...
except Exception:
    ...

resp_data = token_resp.json()
access_token = resp_data['access_token']
```

And that is that!


## Extended Discussion


TODO
