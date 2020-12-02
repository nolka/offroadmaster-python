from abc import ABC, abstractmethod


class Arsenal:
    def __init__(self, weapons=None, active_weapon=None):
        self._weapons = dict() if weapons is None else weapons
        self._active_weapon = None if active_weapon is None else active_weapon

    def add_weapon(self, weapon):
        self._weapons[weapon.name.lower()] = weapon

    def get_weapons_count(self):
        return len(self._weapons)

    def set_active_weapon(self, weapon_name):
        self._active_weapon = self.get_weapon_by_name(weapon_name)

    def get_active_weapon(self):
        return self._active_weapon

    def get_weapon_by_name(self, weapon_name):
        for k, v in self._weapons:
            if k.tolower() == weapon_name.tolower():
                return v


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
