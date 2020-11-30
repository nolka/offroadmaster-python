from abc import ABC

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


class BaseState(ABC):
    def __init__(self, fsm, context):
        self.fsm = fsm
        if context is None:
            self.context = dict()
        else:
            self.context = context

    def update(self, update: Update, context: CallbackContext):
        pass