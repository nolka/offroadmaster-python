import math
import re
import time
from os import getenv

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from states.base_state import BaseState
from states.contexts import SelectGunnerCtx

from transitions import SELECT_GUNNER


class LoadWeapon(BaseState):
    def render_bar(self, bar_size, capacity, charge, charged_cell='▣', empty_cell='▢'):
        charge_value = math.ceil((bar_size / capacity) * charge)
        charged_bar = charged_cell * int(charge_value)
        uncharged = empty_cell * (bar_size - len(charged_bar))
        return charged_bar + uncharged

    def update(self, update: Update, context: CallbackContext):
        message = 'Посылатель заряжается...'
        if not hasattr(self, 'r'):
            self.r = re.compile(r'^заряжа+й!*', re.IGNORECASE)

        if not self.r.match(update.message.text.lower()):
            return
        initial_message_id = update.message.message_id

        capacity = 15
        charge_time = int(getenv('WEAPON_CHARGE_TIME'))
        wait_time = charge_time / capacity
        bar_size = 15
        last_msg = None
        last_message_to_send = ''
        for charge in range(capacity + 1):
            rendered_bar = self.render_bar(bar_size, capacity, charge, )
            last_message_to_send = f'{message}\n`{rendered_bar}`'

            if last_msg is None:
                last_msg = context.bot.send_message(
                    chat_id=update.effective_chat.id, text=last_message_to_send, parse_mode='markdown')
                continue

            if last_msg.text_markdown == last_message_to_send:
                time.sleep(wait_time)
                continue

            last_msg = context.bot.edit_message_text(
                chat_id=update.effective_chat.id, text=last_message_to_send, message_id=last_msg.message_id,
                parse_mode='markdown')

            time.sleep(wait_time)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Посылатель полностью заряжен! Требуется наводчик! Для этого ответь на любое его сообщение!',
                                 reply_to_message_id=initial_message_id)

        self.fsm.transition(SELECT_GUNNER, SelectGunnerCtx(
            initial_message_id, update.message.from_user.name, update.message.from_user.id))
