import re
import random
from functools import wraps


class DiceError(Exception):
    pass


class EmptyDiceError(DiceError):
    pass


class BaseDiceError(DiceError):
    pass


class CountDiceError(DiceError):
    pass


class BonusDiceError(DiceError):
    pass


class Dice(object):
    """
    It makes it possible to operate with dices with same base.
    <count>d<base>
    You can stack the Dice with the same base.
    Dice("1d6") + Dice("2d6") -> Dice("3d6")
    Dice("3d6") + Dice("1d6") -> Dice("2d6")
    """

    def __init__(self, count=0, base=0):
        if not isinstance(count, int):
            dice_dict = self.search_dice_in_str(count)
        else:
            dice_dict = {'count': count, 'base': base}
        if self._is_count_valid(count=dice_dict['count']):
            self.count = dice_dict['count']
        if self._is_base_valid(base=dice_dict['base']):
            self.base = dice_dict['base']

    def __call__(self):
        return self.roll()

    def __str__(self):
        dice_str = "{:d}d{:d}".format(self.count, self.base)
        return dice_str

    def __repr__(self):
        return "Dice({})".format(self.__str__())

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.base != other.base:
                raise BaseDiceError("there is different dice base")
            dice = Dice(count=self.count + other.count, base=self.base)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            if self.base != other.base:
                raise BaseDiceError("there is different dice base")
            dice = Dice(count=self.count - other.count, base=self.base)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    # Setting
    @staticmethod
    def search_dice_in_str(dice_str):
        if not isinstance(dice_str, str):
            try:
                dice_str = str(dice_str)
            except TypeError:
                raise TypeError("unsupported operand type for search_dice_in_str: '{}'".format(type(dice_str)))
        dice_search = re.match(r"^(?P<count>\d+)d(?P<base>\d+)$", dice_str)
        if dice_search:
            return {k: int(v) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_dice(self, count, base=0):
        """
        Run init for set Dice
        """
        self.__init__(count=count, base=base)

    def set_base(self, base=0):
        """
        Set dice base for Dice
        """
        if self._is_base_valid(base=base):
            self.base = base

    def set_count(self, count=0):
        """
        Set count of dice for Dice
        """
        if self._is_count_valid(count=count):
            self.count = count

    # Validating
    @staticmethod
    def _is_count_valid(count):
        """
        Check Dice for validity by dice count.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(count, int):
            raise CountDiceError("unsupported type for dice count: '%s'" % type(count))
        elif count < 0:
            raise CountDiceError("dice count can not be less than zero")
        return True

    def _is_self_count_valid(self):
        return self._is_count_valid(count=self.count)

    @staticmethod
    def _is_base_valid(base):
        """
        Check Dice for validity by dice base.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(base, int):
            raise BaseDiceError("unsupported type for dice base: '%s'" % type(base))
        elif base < 0:
            raise BaseDiceError("dice base can not be less than zero")
        return True

    def _is_self_base_valid(self):
        return self._is_base_valid(base=self.base)

    def _is_dice_valid(self):
        """
        Check Dice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if self._is_self_count_valid() and self._is_self_base_valid():
            return True

    # Dice roll functionality
    def roll(self):
        """
        Roll Dice and return result
        """
        if self._is_dice_valid():
            roll_result = 0
            for i in range(self.count):
                roll_result += random.randint(1, self.base)
            return roll_result

    def max(self):
        """
        Return the maximum value which can be
        """
        if self._is_dice_valid():
            return self.base * self.count

    def min(self):
        """
        Return the minimum value which can be
        """
        if self._is_dice_valid():
            return self.count


class GurpsDice(Dice):
    """
    It makes it possible to operate with dices with base equal 6.
    <count>d6±<bonus>
    or
    <count>d6
    On the addition of number increases the bonus. Similarly, when subtracting.
    GurpsDice("1d6+1") + 1 -> GurpsDice("1d6+2")
    GurpsDice("1d6+1") - 2 -> GurpsDice("1d6-1")
    You can stack the GurpsDice.
    GurpsDice("1d6-1") + GurpsDice("2d6+3") -> GurpsDice("3d6+2")
    GurpsDice("3d6+3") - GurpsDice("1d6-1") -> GurpsDice("2d6+4")
    """

    def __init__(self, count=1, base=6, bonus=0):
        super(GurpsDice, self).__init__(count=count, base=base)
        bonus = bonus if isinstance(count, int) else self.search_dice_in_str(count)['bonus']
        if self._is_bonus_valid(bonus=bonus):
            self.bonus = bonus

    def __str__(self):
        dice_str = super(GurpsDice, self).__str__()
        if self.bonus:
            dice_str += "{:+d}".format(self.bonus)
        return dice_str

    def __repr__(self):
        return "GurpsDice({})".format(self.__str__())

    def __add__(self, other):
        if isinstance(other, self.__class__):
            dice = GurpsDice(count=self.count + other.count, bonus=self.bonus + other.bonus)
        elif isinstance(other, int):
            dice = GurpsDice(count=self.count, bonus=self.bonus + other)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))
        return dice

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            dice = GurpsDice(count=self.count - other.count, bonus=self.bonus - other.bonus)
        elif isinstance(other, int):
            dice = GurpsDice(count=self.count, bonus=self.bonus - other)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))
        return dice

    # Setting
    @staticmethod
    def search_dice_in_str(dice_str):
        if not isinstance(dice_str, str):
            try:
                dice_str = str(dice_str)
            except TypeError:
                raise TypeError("unsupported operand type for search_dice_in_str: '{}'".format(type(dice_str)))
        dice_search = re.match(
            r"^(?P<count>\d+)d(?P<base>[6])(?P<bonus>[-,+]\d+)?$",
            dice_str
        )
        if dice_search:
            return {k: int(v or 0) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_dice(self, count, base=6, bonus=0):
        """
        Run init for set Dice
        """
        self.__init__(count=count, base=base, bonus=bonus)

    def set_base(self, base=6):
        """
        Set dice base for Dice
        """
        if self._is_base_valid(base=base):
            self.base = base

    def set_count(self, count=1):
        """
        Set count of dice for Dice
        """
        super(GurpsDice, self).set_count(count=count)

    def set_bonus(self, bonus):
        """
        Set bonus for GurpsDice
        """
        if self._is_bonus_valid(bonus=bonus):
            self.bonus = bonus

    # Validating
    @staticmethod
    def _is_base_valid(base):
        """
        Check Dice for validity by dice base.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if base != 6:
            raise BaseDiceError("dice base should be equal to 6")
        return True

    def _is_self_base_valid(self):
        return self._is_base_valid(base=self.base)

    @staticmethod
    def _is_bonus_valid(bonus):
        """
        Check GurpsDice for validity by bonus.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(bonus, int):
            raise BonusDiceError("unsupported type for dice base: '%s'" % type(bonus))
        return True

    def _is_self_bonus_valid(self):
        return self._is_bonus_valid(bonus=self.bonus)

    def _is_dice_valid(self):
        """
        Check GurpsDice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        base_and_count_valid = super(GurpsDice, self)._is_dice_valid()
        if base_and_count_valid and self._is_self_bonus_valid():
            return True

    # GurpsDise rounding
    def _add_gurps_dice(self, round_seven=True):
        """
        Added one dice to GurpsDice and balance it
        """
        if self.bonus > 0 and 7 - self.bonus % 7 >= 4 and round_seven:
            self.bonus -= 3
        else:
            self.bonus -= 4
        self.count += 1

    def _remove_gurps_dice(self, round_seven=True):
        """
        Remove one dice from GurpsDice and balance it
        """
        if self.bonus > 0 and self.bonus % 7 >= 4 and round_seven:
            self.bonus += 3
        else:
            self.bonus += 4
        self.count -= 1

    def round_up_step(self, round_seven=True):
        """
        Make one step of GurpsDice equivalenting
        It's round up GurpsDice
        """
        if self._is_dice_valid():
            if self.bonus >= self.bonus >= 3 if round_seven else 4:
                self._add_gurps_dice(round_seven)

    def round_up_max(self, round_seven=True):
        """
        Make GurpsDice absolute equivalenting
        It's round max up GurpsDice
        """
        if self._is_dice_valid():
            while self.bonus >= 3 if round_seven else 4:
                self._add_gurps_dice(round_seven)

    def round_down_step(self, round_seven=True):
        """
        Make one step of GurpsDice equivalenting
        It's round down GurpsDice
        """
        if self._is_dice_valid():
            if self.bonus <= -2 and self.count > 1:
                self._remove_gurps_dice(round_seven)

    def round_down_max(self, round_seven=True):
        """
        Make GurpsDice absolute equivalenting
        It's round max down GurpsDice
        """
        if self._is_dice_valid():
            while self.bonus <= -2 and self.count > 1:
                self._remove_gurps_dice(round_seven)

    def round(self, round_seven=True):
        """
        Make GurpsDice absolute equivalenting
        It's round max up and down GurpsDice
        """
        self.round_up_max(round_seven)
        self.round_down_max(round_seven)

    # GurpsDice roll functionality
    def roll(self):
        """
        Roll GurpsDice and return result
        """
        roll_result = super(GurpsDice, self).roll()
        return roll_result + self.bonus

    def max(self):
        """
        Return the maximum value which can be
        """
        max_result = super(GurpsDice, self).max()
        return max_result + self.bonus

    def min(self):
        """
        Return the minimum value which can be
        """
        min_result = super(GurpsDice, self).min()
        return min_result + self.bonus
