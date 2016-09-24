from pyramid import authentication as base_auth

from kinto.core.storage import exceptions as storage_exceptions


def account_check(username, password, request):
    try:
        print username, password
        existing = request.registry.storage.get(parent_id='',
                                                collection_id='account',
                                                object_id=username)
    except storage_exceptions.RecordNotFound:
        return None
    # XXX: bcrypt whatever
    if existing['password'] == password:
        return True  # anything but None.


class AccountsAuthenticationPolicy(base_auth.BasicAuthAuthenticationPolicy):
    """Accounts authentication policy.

    It will check that the credentials exist in the account resource.
    """
    def __init__(self, *args, **kwargs):
        super(AccountsAuthenticationPolicy, self).__init__(account_check, *args, **kwargs)

    def effective_principals(self, request):
        # Bypass default Pyramid construction of principals because
        # Pyramid multiauth already adds userid, Authenticated and Everyone
        # principals.
        return []
