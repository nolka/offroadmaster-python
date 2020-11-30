import datetime
import random
from os import getenv

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from transitions import WaitCommandTransition


class ReadyToFire(BaseState):
    def __init__(self, fsm, context):
        super().__init__(fsm, context)
        self.started_at = datetime.datetime.now().timestamp()
        self.timeout = int(getenv('SELECT_VICTIM_TIMEOUT'))

    def get_random_phrase(self, victim_name, custom_message=None):
        phrases = (
            '{victim_name}, проследуйте пожалуйста нахуй ☺️',
            'Со звуком "Птиууу!" {victim_name} удалился в сторону хуя 🙈',
            '{victim_name}, ты слышал звук "Чпоньк"? Оглянись, ты присел на бутылку 🍼',
            'Иди нахуй, {victim_name}!',
        )
        if custom_message is not None:
            return custom_message.format(victim_name=victim_name)
        else:
            return phrases[random.randint(0, len(phrases)-1)].format(victim_name=victim_name)

    def update(self, update: Update, context: CallbackContext):
        current_date = datetime.datetime.now().timestamp()
        if current_date - self.started_at >= self.timeout:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.get_random_phrase(self.context.gunner_name, '{victim_name} пошел нахуй...'))
            self.fsm.transition(WaitCommandTransition)
            return

        if update.message.from_user.id != self.context.gunner_id:
            return

        if update.message.reply_to_message is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Нужно именно ответить на любое сообщение цели',
                                     reply_to_message_id=update.message.message_id)
            return

        if 'огонь' not in update.message.text.lower():
            return

        victim_name = update.message.reply_to_message.from_user.name
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.get_random_phrase(victim_name))

        self.fsm.transition(WaitCommandTransition)