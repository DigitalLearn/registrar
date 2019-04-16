""" General utilities for unit tests. """

import json

from django.conf import settings
import responses


def mock_oauth_login(fn):
    """
    Mock request to authenticate registrar as a backend client
    """
    # pylint: disable=missing-docstring
    def inner(self, *args, **kwargs):
        responses.add(
            responses.POST,
            settings.LMS_BASE_URL + '/oauth2/access_token',
            body=json.dumps({'access_token': 'abcd', 'expires_in': 60}),
            status=200
        )
        fn(self, *args, **kwargs)
    return inner
