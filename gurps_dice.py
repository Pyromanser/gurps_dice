import re
import random


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

    def __init__(self, dice_str=None):
        if dice_str:
            founded_dices = self.search_dice_in_str(dice_str)
        else:
            founded_dices = {'count': 0, 'base': 0}
        self.count, self.base = founded_dices['count'], founded_dices['base']

    def __str__(self):
        dice_str = "{:d}d{:d}".format(self.count, self.base)
        return dice_str

    def __repr__(self):
        return "Dice({})".format(self.__str__())

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.base != other.base:
                raise BaseDiceError("there is different dice base")
            dice = Dice()
            dice.set_base(self.base)
            dice.set_count(self.count + other.count)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            if self.base != other.base:
                raise BaseDiceError("there is different dice base")
            dice = Dice()
            dice.set_base(self.base)
            dice.set_count(self.count - other.count)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    # Setting
    @staticmethod
    def search_dice_in_str(dice_str):
        if not isinstance(dice_str, str):
            raise TypeError("unsupported operand type for search_dice_in_str: '{}'".format(type(dice_str)))
        dice_search = re.match(
            r"^(?P<count>\d+)d(?P<base>\d+)$",
            dice_str
        )
        if dice_search:
            return {k: int(v) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_dice(self, dice_str):
        """
        Run init for set Dice
        """
        self.__init__(dice_str)

    def set_base(self, base):
        """
        Set dice base for Dice
        """
        if not isinstance(base, int):
            raise TypeError("unsupported operand type for set_base: '{}'".format(type(base)))
        elif base < 0:
            raise BaseDiceError("dice base can not be less than zero")
        self.base = base

    def set_count(self, count):
        """
        Set count of dice for Dice
        """
        if not isinstance(count, int):
            raise TypeError("unsupported operand type for set_base: '{}'".format(type(count)))
        elif count < 0:
            raise CountDiceError("dice count can not be less than zero")
        self.count = count

    # Validating
    def _is_count_valid(self):
        """
        Check Dice for validity by dice count.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(self.count, int):
            raise CountDiceError("unsupported type for dice count: '%s'" % type(self.count))
        elif self.count < 0:
            raise CountDiceError("dice count can not be less than zero")
        return True

    def _is_base_valid(self):
        """
        Check Dice for validity by dice base.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(self.base, int):
            raise BaseDiceError("unsupported type for dice base: '%s'" % type(self.base))
        elif self.base < 0:
            raise BaseDiceError("dice base can not be less than zero")
        return True

    def _is_dice_valid(self):
        """
        Check Dice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if self._is_count_valid() and self._is_base_valid():
            return True

    # Dice functionality
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
    On the addition of number increases the bonus. Similarly, when subtracting.
    GurpsDice("1d6+1") + 1 -> GurpsDice("1d6+2")
    GurpsDice("1d6+1") - 2 -> GurpsDice("1d6-1")
    You can stack the GurpsDice.
    GurpsDice("1d6-1") + GurpsDice("2d6+3") -> GurpsDice("3d6+2")
    GurpsDice("3d6+3") - GurpsDice("1d6-1") -> GurpsDice("2d6+4")
    """

    def __init__(self, dice_str=None):
        super(GurpsDice, self).__init__(dice_str=None)
        if dice_str:
            founded_dices = self.search_dice_in_str(dice_str)
        else:
            founded_dices = {'count': 1, 'base': 6, 'bonus': 0}
        self.count, self.base, self.bonus = founded_dices['count'], founded_dices['base'], founded_dices['bonus']

    def __str__(self):
        dice_str = super(GurpsDice, self).__str__()
        if self.bonus:
            dice_str += "{:+d}".format(self.bonus)
        return dice_str

    def __add__(self, other):
        dice = GurpsDice()
        dice.set_base(self.base)
        if isinstance(other, self.__class__):
            dice.set_count(self.count + other.count)
            dice.set_bonus(self.bonus + other.bonus)
            return dice
        elif isinstance(other, int):
            dice.set_count(self.count)
            dice.set_bonus(self.bonus + other)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __sub__(self, other):
        dice = GurpsDice()
        dice.set_base(self.base)
        if isinstance(other, self.__class__):
            dice.set_count(self.count - other.count)
            dice.set_bonus(self.bonus - other.bonus)
            return dice
        elif isinstance(other, int):
            dice.set_count(self.count)
            dice.set_bonus(self.bonus - other)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    # Setting
    @staticmethod
    def search_dice_in_str(dice_str):
        if not isinstance(dice_str, str):
            raise TypeError("unsupported operand type for search_dice_in_str: '{}'".format(type(dice_str)))
        dice_search = re.match(
            r"^(?P<count>\d+)d(?P<base>[6])(?P<bonus>[-,+]\d+)?$",
            dice_str
        )
        if dice_search:
            return {k: int(v) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_base(self, base):
        """
        Set dice base for Dice
        """
        if base != 6:
            raise BaseDiceError("dice base should be equal to 6")
        self.base = base

    def set_bonus(self, bonus):
        """
        Set bonus for Dice
        """
        if not isinstance(bonus, int):
            raise TypeError("unsupported operand type for set_base: '{}'".format(type(bonus)))
        self.bonus = bonus

    # Validating
    def _is_bonus_valid(self):
        """
        Check Dice for validity by bonus.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(self.bonus, int):
            raise BonusDiceError("unsupported type for dice base: '%s'" % type(self.bonus))
        return True

    def _is_dice_valid(self):
        """
        Check Dice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        base_and_count_valid = super(GurpsDice, self)._is_dice_valid()
        if base_and_count_valid and self._is_bonus_valid():
            return True

    # Dice functionality
    def roll(self):
        """
        Roll Dice and return result
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
