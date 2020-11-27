from abc import ABC, abstractmethod

class WeaponCollection:
    def __init__(self):
        self.weapons = dict()

    def add_weapon(self, weapon):
        self.weapons[weapon.name.lower()] = weapon

class WeaponAbstract(ABC):
    name = "Weapon"

    @property
    @abstractmethod
    def battery_capacity(self):
        pass

    @property
    @abstractmethod
    def charge_time(self):
        pass

class IdiNakhui(WeaponAbstract):
    name = 'Посылатель'

    @property
    def battery_capacity(self):
        return 15

    @property
    def charge_time(self):
        return 25