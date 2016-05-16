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
    <count>d<base>+<bonus>
    or
    <count>d<base>
    On the addition of number increases the bonus. Similarly, when subtracting.
    Dice("1d6+1") + 1 = Dice("1d6+2")
    You can stack the Dice with the same base.
    Dice("1d6+1") + Dice("2d6+3") = Dice("3d6+4")
    """

    count = 0
    base = 0
    bonus = 0

    def __init__(self, dice_str=None):
        if dice_str:
            dice_search = re.match(
                # r"^(?P<count>[1-9][0-9]*)d(?P<base>[1-9][0-9]*)(?P<bonus>[-,+][1-9][0-9]*)?$",
                r"^(?P<count>\d+)d(?P<base>\d+)(?P<bonus>[-,+]\d*)?$",
                dice_str
            )
            if dice_search:
                dice = dice_search.groupdict()
                self.count, self.base = int(dice['count']), int(dice['base'])
                if dice['bonus']:
                    self.bonus = int(dice['bonus'])
            else:
                raise EmptyDiceError("there is no correct dice param in str")

    def __str__(self):
        dice_str = "%dd%d" % (self.count, self.base)
        if self.bonus:
            dice_str += "%+d" % self.bonus
        return dice_str

    def __repr__(self):
        return "Dice(" + self.__str__() + ")"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.base != other.base:
                raise BaseDiceError("there is different dice base")
            dice = Dice()
            dice.set_base(self.base)
            dice.set_count(self.count + other.count)
            dice.set_bonus(self.bonus + other.bonus)
            return dice
        elif isinstance(other, int):
            dice = Dice()
            dice.set_base(self.base)
            dice.set_count(self.count)
            dice.set_bonus(self.bonus + other)
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
            dice.set_bonus(self.bonus - other.bonus)
            return dice
        elif isinstance(other, int):
            dice = Dice()
            dice.set_base(self.base)
            dice.set_count(self.count)
            dice.set_bonus(self.bonus - other)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

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

    def set_bonus(self, bonus):
        """
        Set bonus for Dice
        """
        if not isinstance(bonus, int):
            raise TypeError("unsupported operand type for set_base: '{}'".format(type(bonus)))
        self.bonus = bonus

    def roll(self):
        """
        Roll Dice and return result
        """
        if self._is_dice_valid():
            roll_result = 0
            if self.bonus:
                roll_result += self.bonus
            for i in range(self.count):
                roll_result += random.randint(1, self.base)
            return roll_result

    def max(self):
        """
        Return the maximum value which can be
        """
        if self._is_dice_valid():
            return self.base * self.count + self.bonus

    def min(self):
        """
        Return the minimum value which can be
        """
        if self._is_dice_valid():
            return self.count + self.bonus

    def equiv(self, round_seven=True):
        """
        Make one step of Dice equivalenting
        It's round up and down Dice
        """
        self.equiv_up(round_seven)
        self.equiv_down()

    def equiv_max(self, round_seven=True):
        """
        Make Dice absolute equivalenting
        It's round max up and down Dice
        """
        self.equiv_up_max(round_seven)
        self.equiv_down_max()

    def equiv_up(self, round_seven=True):
        """
        Make one step of Dice equivalenting
        It's round up Dice
        """
        if self._is_dice_valid():
            if self.bonus >= 7 and round_seven:
                self.bonus -= 7
                self.count += 2
            elif self.bonus >= 4:
                self._add_dice()
            elif self.bonus == 3:
                self._add_dice()

    def equiv_up_max(self, round_seven=True):
        """
        Make Dice absolute equivalenting
        It's round max up Dice
        """
        if self._is_dice_valid():
            if self.bonus >= 7 and round_seven:
                multiplier = self.bonus // 7
                self.bonus -= 7 * multiplier
                self.count += 2 * multiplier
            while self.bonus >= 3:
                self._add_dice()

    def equiv_down(self):
        """
        Make one step of Dice equivalenting
        It's round down Dice
        """
        if self._is_dice_valid():
            if self.bonus <= -2 and self.count > 1:
                self._remove_dice()

    def equiv_down_max(self):
        """
        Make Dice absolute equivalenting
        It's round max down Dice
        """
        if self._is_dice_valid():
            while self.bonus <= -2 and self.count > 1:
                self._remove_dice()

    def _add_dice(self):
        """
        Added one dice to Dice and balance it
        """
        self.bonus -= 4
        self.count += 1

    def _remove_dice(self):
        """
        Remove one dice from Dice and balance it
        """
        self.bonus += 4
        self.count -= 1

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
        if self._is_count_valid() and self._is_base_valid() and self._is_bonus_valid():
            return True