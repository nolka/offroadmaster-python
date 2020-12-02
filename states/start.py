from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from transitions import WAIT_COMMAND


class Start(BaseState):
    def update(self, update: Update, context: CallbackContext):
        self.fsm.transition(WAIT_COMMAND)
