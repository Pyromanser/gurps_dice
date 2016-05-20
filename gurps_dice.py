import re
import random


class DiceError(Exception):
    pass


class EmptyDiceError(DiceError):
    pass


class DiceFaceError(DiceError):
    pass


class DiceCountError(DiceError):
    pass


class DiceBonusError(DiceError):
    pass


class Dice(object):
    """
    It makes it possible to operate with dices with same face.
    <count>d<face>
    You can stack the Dice with the same face.
    Dice("1d6") + Dice("2d6") -> Dice("3d6")
    Dice("3d6") + Dice("1d6") -> Dice("2d6")
    """

    def __init__(self, count=0, face=0):
        if not isinstance(count, int):
            dice_dict = self.search_dice_in_str(count)
        else:
            dice_dict = {'count': count, 'face': face}
        if self._is_count_valid(count=dice_dict['count']):
            self.count = dice_dict['count']
        if self._is_face_valid(face=dice_dict['face']):
            self.face = dice_dict['face']

    def __call__(self):
        return self.roll()

    def __str__(self):
        dice_str = "{:d}d{:d}".format(self.count, self.face)
        return dice_str

    def __repr__(self):
        return "Dice({})".format(self.__str__())

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.face != other.face:
                raise DiceFaceError("there is different dice face")
            dice = Dice(count=self.count + other.count, face=self.face)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            if self.face != other.face:
                raise DiceFaceError("there is different dice face")
            dice = Dice(count=self.count - other.count, face=self.face)
            return dice
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(self.__class__, type(other)))

    # Setting
    @staticmethod
    def search_dice_in_str(dice_str):
        if not isinstance(dice_str, str):
            try:
                dice_str = str(dice_str)
            except TypeError:
                raise TypeError("unsupported operand type for search_dice_in_str: '{}'".format(type(dice_str)))
        dice_search = re.match(r"^(?P<count>\d+)d(?P<face>\d+)$", dice_str)
        if dice_search:
            return {k: int(v) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_dice(self, count, face=0):
        """
        Run init for set Dice
        """
        self.__init__(count=count, face=face)

    def set_face(self, face=0):
        """
        Set dice face for Dice
        """
        if self._is_face_valid(face=face):
            self.face = face

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
            raise DiceCountError("unsupported type for dice count: '%s'" % type(count))
        elif count < 0:
            raise DiceCountError("dice count can not be less than zero")
        return True

    def _is_self_count_valid(self):
        return self._is_count_valid(count=self.count)

    @staticmethod
    def _is_face_valid(face):
        """
        Check Dice for validity by dice face.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(face, int):
            raise DiceFaceError("unsupported type for dice face: '%s'" % type(face))
        elif face < 0:
            raise DiceFaceError("dice face can not be less than zero")
        return True

    def _is_self_face_valid(self):
        return self._is_face_valid(face=self.face)

    def _is_dice_valid(self):
        """
        Check Dice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if self._is_self_count_valid() and self._is_self_face_valid():
            return True

    # Dice roll functionality
    def roll(self):
        """
        Roll Dice and return result
        """
        if self._is_dice_valid():
            roll_result = 0
            if self.face:
                for i in range(self.count):
                    roll_result += random.randint(1, self.face)
            return roll_result

    def max(self):
        """
        Return the maximum value which can be
        """
        if self._is_dice_valid():
            return self.face * self.count

    def min(self):
        """
        Return the minimum value which can be
        """
        if self._is_dice_valid():
            return self.count if self.face else 0


class GurpsDice(Dice):
    """
    It makes it possible to operate with dices with face equal 6.
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

    def __init__(self, count=1, bonus=0):
        super(GurpsDice, self).__init__(count=count, face=6)
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
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(self.__class__, type(other)))
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
            r"^(?P<count>\d+)d(?P<face>[6])(?P<bonus>[-,+]\d+)?$",
            dice_str
        )
        if dice_search:
            return {k: int(v or 0) for k, v in dice_search.groupdict().items()}
        else:
            raise EmptyDiceError("there is no correct dice param in str")

    def set_dice(self, count, bonus=0):
        """
        Run init for set Dice
        """
        self.__init__(count=count, bonus=bonus)

    def set_face(self, *args, **kwargs):
        """
        Removed method for GurpsDice
        """
        raise DiceFaceError("dice face can not be changed")

    def set_count(self, count=1):
        """
        Set count of dice for GurpsDice
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
    def _is_face_valid(face):
        """
        Check Dice for validity by dice face.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if face != 6:
            raise DiceFaceError("dice face should be equal to 6")
        return True

    def _is_self_face_valid(self):
        return self._is_face_valid(face=self.face)

    @staticmethod
    def _is_bonus_valid(bonus):
        """
        Check GurpsDice for validity by bonus.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        if not isinstance(bonus, int):
            raise DiceBonusError("unsupported type for dice face: '%s'" % type(bonus))
        return True

    def _is_self_bonus_valid(self):
        return self._is_bonus_valid(bonus=self.bonus)

    def _is_dice_valid(self):
        """
        Check GurpsDice for whole validity.
        Return True if it's Ok
        Rise error's if something not Ok
        """
        face_and_count_valid = super(GurpsDice, self)._is_dice_valid()
        if face_and_count_valid and self._is_self_bonus_valid():
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
