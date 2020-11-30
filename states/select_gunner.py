import datetime
from os import getenv

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from states.contexts import FireCtx
from transitions import ReadyToFireTransition, WaitCommandTransition


class SelectGunner(BaseState):
    def __init__(self, fsm, context):
        super().__init__(fsm, context)
        self.started_at = datetime.datetime.now().timestamp()
        self.timeout = int(getenv('SELECT_GUNNER_TIMEOUT'))

    def update(self, update: Update, context: CallbackContext):
        current_date = datetime.datetime.now().timestamp()
        if current_date - self.started_at >= self.timeout:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{self.context.initiator_name} не смог! Орудие разряжено!')
            self.fsm.transition(WaitCommandTransition)

        if update.message.from_user.id != self.context.initiator_id:
            return
        if update.message.reply_to_message is None:
            return

        gunner_name = update.message.reply_to_message.from_user.name
        self.commander_name = update.message.from_user.name
        self.comander_id = update.message.from_user.id
        selected_gunner_message = f'{update.message.from_user.name} Выбрал в качестве наводчика {gunner_name}! Для того, чтобы выстрелить наводчик должен ответить на любое сообщение цели фразой "Огонь!"'
        context.bot.send_message(chat_id=update.effective_chat.id, text=selected_gunner_message,
                                 reply_to_message_id=update.message.message_id)
        self.fsm.transition(ReadyToFireTransition, FireCtx(
            gunner_name, update.message.reply_to_message.from_user.id))