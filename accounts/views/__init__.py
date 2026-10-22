from .register_views import RegisterView
from .register_done_views import RegisterDoneView
from .account_delete_views import AccountDeletionView
from .account_delete_done_views import AccountDeletionDoneView
from .login_views import AccountLoginView

__all__ = [
    'RegisterView',
    'RegisterDoneView',
    'AccountLoginView',
    'AccountDeletionView',
    'AccountDeletionDoneView',
]