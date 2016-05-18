from gurps_dice import Dice


class HandfulDiceError(Exception):
    pass


class HandfulDice(object):
    def __init__(self, *args, bonus=0):
        for dice in args:
            if not isinstance(dice, Dice):
                raise TypeError("unsupported type for dice: '{}'".format(type(dice)))
        self.handful = args
        if not isinstance(bonus, int):
            raise TypeError("unsupported type for bonus: '{}'".format(type(bonus)))
        self.bonus = bonus

    def __str__(self):
        handful_dice_str = '+'.join(self.handful)
        if self.bonus:
            handful_dice_str += "{:+d}".format(self.bonus)
        return handful_dice_str

    def __repr__(self):
        return 'HandfulDice({})'.format(self.__str__())

    def __add__(self, other):
        if isinstance(other, int):
            return HandfulDice(self.handful, bonus=self.bonus + other)
        elif isinstance(other, Dice):
            return HandfulDice(*(self.handful + (other,)), bonus=self.bonus)
        elif isinstance(other, self.__class__):
            return HandfulDice(*(self.handful + other.handful), bonus=self.bonus + other.bonus)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __sub__(self, other):
        if isinstance(other, int):
            return HandfulDice(self.handful, bonus=self.bonus - other)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(self.__class__, type(other)))

    def add_dice(self, dice):
        if isinstance(dice, str):
            self.add_dice(Dice(dice))
        elif isinstance(dice, Dice):
            self.handful += (dice,)
        else:
            raise TypeError("unsupported type for add_dice: '{}'".format(type(dice)))
