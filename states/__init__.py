import logging

from transitions import TransitionDef, START, WAIT_COMMAND, LOAD_WEAPON, \
    SELECT_GUNNER, FIRE

from states.load_weapon import LoadWeapon
from states.fire import Fire
from states.select_gunner import SelectGunner
from states.start import Start
from states.wait_command import WaitCommand


class FSM:
    transitions = {
        START: TransitionDef((Start,), Start),
        WAIT_COMMAND: TransitionDef((Start, Fire, LoadWeapon, SelectGunner), WaitCommand),
        LOAD_WEAPON: TransitionDef((WaitCommand,), LoadWeapon),
        SELECT_GUNNER: TransitionDef((LoadWeapon,), SelectGunner),
        FIRE: TransitionDef((SelectGunner,), Fire),
    }

    def __init__(self, init_state):
        self.current_state = None
        self.set_state(init_state)

    def set_state(self, new_state, context=None):
        self.current_state = new_state(self, context)

    def get_state(self):
        return self.current_state

    def transition(self, trans, context=None):
        if trans not in self.transitions:
            logging.error(f'No transition found: {trans}')
            return

        transition_data = self.transitions[trans]
        current_state_name = self.get_state().__class__.__name__
        if self.get_state().__class__ not in transition_data.src:
            logging.error(
                f'Cannot make transition to state {trans} from {current_state_name}')
            return

        self.set_state(transition_data.dest, context)
