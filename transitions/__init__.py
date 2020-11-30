class TransitionDef:
    __slots__ = ('src', 'dest')

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class BaseTransition:
    pass


class StartTransition(BaseTransition):
    pass


class WaitCommandTransition:
    pass


class LoadWeaponTransition:
    pass


class SelectGunnerTransition:
    pass


class ReadyToFireTransition(BaseTransition):
    pass
