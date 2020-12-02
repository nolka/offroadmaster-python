class TransitionDef:
    __slots__ = ('src', 'dest')

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


START, WAIT_COMMAND, LOAD_WEAPON, SELECT_GUNNER, FIRE = range(5)
