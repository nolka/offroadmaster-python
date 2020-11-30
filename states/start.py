from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from transitions import WaitCommandTransition



class Start(BaseState):
    def update(self, update: Update, context: CallbackContext):
        self.fsm.transition(WaitCommandTransition)
