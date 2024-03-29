import re
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from transitions import LOAD_WEAPON


class WaitCommand(BaseState):
    def update(self, update: Update, context: CallbackContext):
        if not hasattr(self, 'r'):
            self.r = re.compile(r'^заряжа+й!*', re.IGNORECASE)

        if self.r.match(update.message.text.lower()):
            self.fsm.transition(LOAD_WEAPON)
            self.fsm.get_state().update(update, context)