
class UserActions:
    ASSETS = 'assets'
    SUBSCRIBE = 'subscribe'


class AllActions(UserActions):
    POINT = 'point'


ALLOWED_ACTIONS = {getattr(UserActions, x) for x in dir(UserActions) if not x.startswith('__')}
