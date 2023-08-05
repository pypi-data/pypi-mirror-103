# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkce_flow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'pkce-flow',
    'version': '0.1.2',
    'description': 'A utility for obtaining access tokens using the PKCE-enhanced authorization code flow (Oauth)',
    'long_description': "# PKCE-flow\n\n\nPKCE-flow is a utility for obtaining access tokens using [the PKCE-enhanced authorization code flow (Oauth)](https://tools.ietf.org/html/rfc7636)\n\n\n## Quick Start\n\n\n### First Things First\n\n\nWe'll be walking through the creation of a utility for obtaining an access token that will allow us access GitLab resources on behalf of a particular user.\n\nIf you plan to _work through_ this, then you'll need to take five minutes (approx.) to create an Application with GitLab, so that you can have a client id and secret.\n\nYou can use any other service of your choice which implements PKCE OAuth. The process will be the same.\n\n\n### Creating a PKCEFlowManager Instance\n\n\n#### Subclass the Manager Class\n\n\n```python\nfrom pkce_flow import AbstractBasePKCEFlowManager\n\n\nclass GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):\n    pass\n```\n\n\n#### Configure the Required Attributes\n\n\n```python\nfrom pkce_flow import AbstractBasePKCEFlowManager\n\n\nclass GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):\n    client_id = 'our GitLab application id'\n    client_secret = 'our GitLab application secret'\n    redirect_uri = 'http://127.0.0.1:8000/oauth/gitlab/callback/'\n    root_url = 'https://gitlab.com/oauth/'\n    scope = 'read_api'\n```\n\nA quick description of the attributes we're defining:\n\n* __client_id__: The ID of the developer application that will be requesting access to the resources on the user's behalf. The application must have been already created by the developer with the service.\n\n* __client_secret__: The SECRET KEY of the developer application.\n\n* __redirect_uri__: The redirect uri or callback uri that was specified by the developer when they created the developer application.\n\n* __root_url__: The base url for authentication with the service.\n\n* __scope__: Space delimited permission scopes.\n\n\n#### Override the _Hook_ Methods\n\n\n```python\nfrom pkce_flow import AbstractBasePKCEFlowManager\n\n\nclass GitLabPKCEFlowManager(AbstractBasePKCEFlowManager):\n    client_id = 'our GitLab application id'\n    client_secret = 'our GitLab application secret'\n    redirect_uri = 'http://127.0.0.1:8000/oauth/gitlab/callback/'\n    root_url = 'https://gitlab.com/oauth/'\n    scope = 'read_api'\n\n    def store_user_secrets(self, user, state, code_verifier, code_challenge):\n        # write code to persist the state, code verifier, and code challenge\n        # against the user in a place you can retrieve them later\n        ...\n\n    def retrieve_user_state(self, user):\n        # write code to retrieve the state which was persisted against\n        # the argument user\n        ...\n        return state\n\n    def retrieve_user_code_challenge(self, user):\n        # write code to retrieve the code challenge which was\n        # persisted against the argument user\n        ...\n        return code_challenge\n\n    def retrieve_user_code_verifier(self, user):\n        # write code to retrieve the code verifier which was\n        # persisted against the argument user\n        ...\n        return code_verifier\n\n    def check_user_state(self, user, state):\n        # write code to check whether argument state is the same as\n        # the state that was persisted against the argument user\n        ...\n        return is_same\n```\n\n\n#### Instantiate a Project-wide Manager from Your Subclass\n\n\n```python\ngitlab_manager = GitLabPKCEFlowManager()\n```\n\n\n### Using the Manager Instance\n\n\nSo, a user of your web app wants to give you permission to access resources on GitLab on their behalf. And you've created a GitLab PKCE-flow manager for this.\n\nThe next thing to do is to make the secrets needed for the PKCE flow.\n\n```python\nstate, verifier, challenge = gitlab_manager.make_user_secrets(user=user)\n```\n\nSince you've already _taught_ your manager how to store secrets against a user, it will store these secrets against the argument user before returning them to you.\n\nAfter this, you get the url which you will send/redirect the user to, so they can authorize your request for an access token on their behalf.\n\n```python\nurl = gitlab_manager.get_authorization_url(user=user)\n```\n\nThen in your web app, in the view which handles the endpoint corresponding to the redirect uri, you extract the `state` and `code` query parameters so you can fetch the user's access token with their values.\n\n```python\nfrom requests.exceptions import RequestException\nfrom pkce_flow.exceptions import StateForgeryException\n\n\nstate = ...  # extract value of the query param 'state' from request\ncode = ...  # extract value of the query param 'code' from request\n\ntry:\n    token_resp = gitlab_manager.fetch_access_token(\n        user=user, state=state, code=code\n    )\nexcept StateForgeryException:\n    ...\nexcept RequestException:\n    ...\nexcept Exception:\n    ...\n\nresp_data = token_resp.json()\naccess_token = resp_data['access_token']\n```\n\nAnd that is that!\n\n\n## Extended Discussion\n\n\nTODO\n",
    'author': 'Mfon Eti-mfon',
    'author_email': 'mfonetimfon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/a-thousand-juniors/pkce-flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
