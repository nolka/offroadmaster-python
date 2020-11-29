import time
import math
import datetime
from abc import ABC
import logging
import random
import re
from os import getenv

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


class Start(BaseState):
    def update(self, update: Update, context: CallbackContext):
        self.fsm.transition(WaitCommand)


class WaitCommand(BaseState):
    def update(self, update: Update, context: CallbackContext):
        if not hasattr(self, 'r'):
            self.r = re.compile(r'^заряжа+й!*', re.IGNORECASE)

        if self.r.match(update.message.text.lower()):
            self.fsm.transition(LoadWeapon)
            self.fsm.get_state().update(update, context)


class SelectGunner(BaseState):
    def __init__(self, fsm, context):
        super().__init__(fsm, context)
        self.started_at = datetime.datetime.now().timestamp()
        self.timeout = int(getenv('SELECT_GUNNER_TIMEOUT'))

    def update(self, update: Update, context: CallbackContext):
        current_date = datetime.datetime.now().timestamp()
        if current_date - self.started_at >= self.timeout:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{self.context.initiator_name} не смог! Орудие разряжено!')
            self.fsm.transition(WaitCommand)

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
        self.fsm.transition(ReadyToFire, FireCtx(
            gunner_name, update.message.reply_to_message.from_user.id))


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
            self.fsm.transition(WaitCommand)
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

        # time.sleep(60*15)
        self.fsm.transition(WaitCommand)


class SelectGunnerCtx:
    def __init__(self, init_msg_id, initiator_name, initiator_id):
        self.init_msg_id = init_msg_id
        self.initiator_name = initiator_name
        self.initiator_id = initiator_id

class FireCtx:
    def __init__(self, gunner_name, gunner_id, custom_message=None):
        self.gunner_name = gunner_name
        self.gunner_id = gunner_id
        self.custom_message = custom_message

class LoadWeapon(BaseState):
    def render_bar(self, bar_size, capacity, charge, charged_cell='▣', empty_cell='▢'):
        charge_value = math.ceil((bar_size/capacity)*charge)
        charged_bar = charged_cell*int(charge_value)
        uncharged = empty_cell*(bar_size-len(charged_bar))
        return charged_bar+uncharged

    def update(self, update: Update, context: CallbackContext):
        message = 'Посылатель заряжается...'
        if not hasattr(self, 'r'):
            self.r = re.compile(r'^заряжа+й!*', re.IGNORECASE)

        if not self.r.match(update.message.text.lower()):
            return
        initial_message_id = update.message.message_id

        capacity = 15
        charge_time = int(getenv('WEAPON_CHARGE_TIME'))
        wait_time = charge_time/capacity
        bar_size = 15
        last_msg = None
        last_message_to_send = ''
        for charge in range(capacity+1):
            rendered_bar = self.render_bar(bar_size, capacity, charge,)
            last_message_to_send = f'{message}\n`{rendered_bar}`'

            if last_msg is None:
                last_msg = context.bot.send_message(
                    chat_id=update.effective_chat.id, text=last_message_to_send, parse_mode='markdown')
                continue

            if last_msg.text_markdown == last_message_to_send:
                time.sleep(wait_time)
                continue

            last_msg = context.bot.edit_message_text(
                chat_id=update.effective_chat.id, text=last_message_to_send, message_id=last_msg.message_id, parse_mode='markdown')

            time.sleep(wait_time)

        context.bot.send_message(chat_id=update.effective_chat.id, text='Посылатель полностью заряжен! Требуется наводчик! Для этого ответь на любое его сообщение!',
                                 reply_to_message_id=initial_message_id)

        self.fsm.transition(SelectGunner, SelectGunnerCtx(
            initial_message_id, update.message.from_user.name,update.message.from_user.id))


class FSM:
    state_list = (
        Start,
        WaitCommand,
        LoadWeapon,
    )
    transitions = {
        Start: {
            'from': (Start, ),
            'to': Start,
        },
        WaitCommand: {
            'from': (Start, ReadyToFire, LoadWeapon, SelectGunner),
            'to': WaitCommand,
        },
        LoadWeapon: {
            'from': (WaitCommand, ),
            'to': LoadWeapon,
        },
        SelectGunner: {
            'from': (LoadWeapon, ),
            'to': SelectGunner,
        },
        ReadyToFire: {
            'from': (SelectGunner, ),
            'to': ReadyToFire,
        }
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
        if self.get_state().__class__ not in transition_data['from']:
            logging.error(
                f'Cannot make transition to state {trans} from {current_state_name}')
            return

        self.set_state(transition_data['to'], context)
