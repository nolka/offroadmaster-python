
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
