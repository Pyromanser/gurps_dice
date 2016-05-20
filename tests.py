import random
from gurps_dice import Dice, GurpsDice, EmptyDiceError, BaseDiceError, CountDiceError
from gurps_dice_handful import HandfulDice


def random_int(start, end, excluding=()):
    r_int = random.randint(start, end)
    if r_int in excluding:
        r_int = random_int(start, end, excluding)
    return r_int


def get_dice_str(count, base, bonus=0):
    dice_str = "{:d}d{:d}".format(count, base)
    if bonus:
        dice_str += "{:+d}".format(bonus)
    return dice_str

if __name__ == "__main__":

    # test Dice

    print("---"*20)
    print("Dice test start")
    print("---"*20)

    dice = Dice()
    assert dice.__str__() == '0d0', 'Dice() != "0d0", Dice() == %s' % dice
    print('Dice() == "0d0", OK')

    for count in range(101):
        for base in range(101):
            dice_str = get_dice_str(count, base)
            dice = Dice(dice_str)
            assert dice.__str__() == dice_str, 'Dice("{dice_str}") != "{dice_str}", Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with count and base parameters in range 0-100 is valid, OK')

    for count in range(101):
        for base in range(101):
            for bonus in (x for x in range(-101, 101) if x != 0):
                dice_str = get_dice_str(count, base, bonus)
                try:
                    dice = Dice(dice_str)
                except EmptyDiceError:
                    pass
                else:
                    assert True, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with count, base and "bonus" parameters in range 0-100 raise EmptyDiceError, OK')

    for count in range(-100, 0):
        for base in range(101):
            dice_str = get_dice_str(count, base)
            try:
                dice = Dice(dice_str)
            except EmptyDiceError:
                pass
            else:
                assert True, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with count in range -100-0 and base in range 0-100 parameters in range 0-100 raise EmptyDiceError, OK')

    for count in range(101):
        for base in range(-100, 0):
            dice_str = get_dice_str(count, base)
            try:
                dice = Dice(dice_str)
            except EmptyDiceError:
                pass
            else:
                assert True, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with count in range 0-100 and base in range -100-0 parameters in range 0-100 raise EmptyDiceError, OK')

    for base in range(101):
        for count in range(101):
            dice_str = get_dice_str(count, base)
            dice = Dice(count, base)
            assert dice.__str__() == dice_str, 'Dice({count}, {base}) != "{dice_str}", Dice({count}, {base}) == {dice}'.format(dice_str=dice_str, count=count, base=base, dice=dice)
    print('Dice(count, base) with count and base parameters in range 0-100 is valid, OK')

    for base in range(101):
        for count1 in range(101):
            for count2 in range(101):
                dice1_str = get_dice_str(count1, base)
                dice2_str = get_dice_str(count2, base)
                dice_str = get_dice_str(count1 + count2, base)
                dice1 = Dice(count1, base)
                dice2 = Dice(count2, base)
                dice = (dice1 + dice2)
                assert dice.__str__() == dice_str, 'Dice({count1}, {base}) + Dice({count2}, {base}) != "{dice_str}", Dice({count1}, {base}) + Dice({count2}, {base}) == {dice}'.format(dice_str=dice_str, count1=count1, count2=count2, base=base, dice=dice)
    print('Dice(count1, base) + Dice(count2, base) with counts and base parameters in range 0-100 is valid, OK')

    for count1 in range(51):
        for count2 in range(51):
            for base1 in range(51):
                for base2 in range(51):
                    if base1 == base2:
                        continue
                    dice1 = Dice(count1, base1)
                    dice2 = Dice(count2, base2)
                    try:
                        dice = (dice1 + dice2)
                    except BaseDiceError:
                        pass
                    else:
                        assert True, 'Dice({count1}, {base1}) + Dice({count2}, {base2}) should raise BaseDiceError, Dice({count1}, {base1}) + Dice({count2}, {base2}) == {dice}'.format(count1=count1, count2=count2, base1=base1, base2=base2, dice=dice)
    print('Dice(count1, base1) + Dice(count2, base2) with count1 and count2 in range 0-50, base1 and base2 in disjoint range 0-50 raise BaseDiceError, OK')

    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 + dice2)
    except TypeError:
        print('Dice(1, 20) + "1d20" raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) + "1d20" should raise TypeError, Dice(1, 20) + "1d20" == %s' % dice

    dice1 = Dice(1, 20)
    bonus = 1
    try:
        dice = (dice1 + bonus)
    except TypeError:
        print('Dice(1, 20) + 1 raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) + 1 should raise TypeError, Dice(1, 20) + 1 == %s' % dice

    for base in range(101):
        for count1 in range(101):
            for count2 in range(101):
                if count2 > count1:
                    continue
                dice_str = get_dice_str(count1 - count2, base)
                dice1 = Dice(count1, base)
                dice2 = Dice(count2, base)
                dice = (dice1 - dice2)
                assert dice.__str__() == dice_str, 'Dice({count1}, {base}) - Dice({count2}, {base}) != "{dice_str}", Dice({count1}, {base}) - Dice({count2}, {base}) == {dice}'.format(dice_str=dice_str, count1=count1, count2=count2, base=base, dice=dice)
    print('Dice(count1, base) - Dice(count2, base) with count1 and count2 on condition count2 > count1 and base parameters in range 0-100 is valid, OK')

    for base in range(101):
        for count1 in range(101):
            for count2 in range(101):
                if count1 > count2:
                    continue
                dice1 = Dice(count1, base)
                dice2 = Dice(count2, base)
                try:
                    dice = (dice1 - dice2)
                except CountDiceError:
                    pass
                else:
                    assert True, 'Dice({count1}, {base}) - Dice({count2}, {base}) should raise CountDiceError, Dice({count1}, {base}) - Dice({count2}, {base}) == {dice}'.format(count1=count1, count2=count2, base=base, dice=dice)
    print('Dice(count1, base) - Dice(count2, base) with count1 and count2 on condition count1 > count2 and base parameters in range 0-100 raise CountDiceError, OK')

    for count1 in range(51):
        for count2 in range(51):
            for base1 in range(51):
                for base2 in range(51):
                    if base1 == base2 or count1 > count2:
                        continue
                    dice1 = Dice(count1, base1)
                    dice2 = Dice(count2, base2)
                    try:
                        dice = (dice1 - dice2)
                    except BaseDiceError:
                        pass
                    else:
                        assert True, 'Dice({count1}, {base1}) - Dice({count2}, {base2}) should raise BaseDiceError, Dice({count1}, {base1}) - Dice({count2}, {base2}) == {dice}'.format(count1=count1, count2=count2, base1=base1, base2=base2, dice=dice)
    print('Dice(count1, base1) - Dice(count2, base2) with count1 and count2 in range 0-50, base1 on condition count2 > count1 and base2 in disjoint range 0-50 raise BaseDiceError, OK')

    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 - dice2)
    except TypeError:
        print('Dice(1, 20) - "1d20" raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) - "1d20" should raise TypeError, Dice(1, 20) - "1d20" == %s' % dice

    dice1 = Dice(1, 20)
    bonus = 1
    try:
        dice = (dice1 - bonus)
    except TypeError:
        print('Dice(1, 20) - 1 raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) - 1 should raise TypeError, Dice(1, 20) - 1 == %s' % dice

    for count in range(101):
        for base in range(101):
            dice_str = get_dice_str(count, base)
            dice = Dice()
            dice.set_dice(dice_str)
            assert dice.__str__() == dice_str, 'dice.set_dice("{dice_str}") != "{dice_str}", dice.set_dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('dice.set_dice("<count>d<base>") with count and base parameters in range 0-100 is valid, OK')

    for count in range(101):
        for base in range(101):
            dice_str = get_dice_str(count, base)
            dice = Dice()
            dice.set_dice(count, base)
            assert dice.__str__() == dice_str, 'dice.set_dice({count}, {base}) != "{dice_str}", dice.set_dice({count}, {base}) == {dice}'.format(dice_str=dice_str, count=count, base=base, dice=dice)
    print('dice.set_dice(count, base) with count and base parameters in range 0-100 is valid, OK')

    for base in range(101):
        dice_str = get_dice_str(0, base)
        dice = Dice()
        dice.set_base(base)
        assert dice.__str__() == dice_str, 'dice.set_base({base}) != "{dice_str}", dice.set_base({base}) == {dice}'.format(dice_str=dice_str, base=base, dice=dice)
    print('dice.set_base(base) with base parameter in range 0-100 is valid, OK')

    for count in range(101):
        dice_str = get_dice_str(count, 0)
        dice = Dice()
        dice.set_count(count)
        assert dice.__str__() == dice_str, 'dice.set_count({count}) != "{dice_str}", dice.set_count({count}) == {dice}'.format(dice_str=dice_str, count=count, dice=dice)
    print('dice.set_count(count) with count parameter in range 0-100 is valid, OK')

    for count in range(1, 101):
        for base in range(1, 101):
            dice_str = get_dice_str(count, base)
            maximum_assert = count * base
            dice = Dice(dice_str)
            maximum = dice.max()
            assert maximum == maximum_assert, 'Dice("{dice_str}").max() != {maximum_assert}, Dice("{dice_str}").max() == {maximum}'.format(dice_str=dice_str, maximum_assert=maximum_assert, maximum=maximum)
    print('Dice("<count>d<base>").max() with count and base parameters in range 1-100 is valid, OK')

    for count in range(1, 101):
        for base in range(1, 101):
            dice_str = get_dice_str(count, base)
            minimum_assert = count
            dice = Dice(dice_str)
            minimum = dice.min()
            assert minimum == minimum_assert, 'Dice("{dice_str}").min() != {minimum_assert}, Dice("{dice_str}").min() == {minimum}'.format(dice_str=dice_str, minimum_assert=minimum_assert, minimum=minimum)
    print('Dice("<count>d<base>").min() with count and base parameters in range 1-100 is valid, OK')

    dice = Dice()
    maximum = dice.max()
    assert maximum == 0, 'Dice().max() != 0, Dice().max() == %s' % maximum
    print('Dice().max() == 0, OK')

    dice = Dice()
    minimum = dice.min()
    assert minimum == 0, 'Dice().min() != 0, Dice().min() == %s' % minimum
    print('Dice().min() == 0, OK')

    dice = Dice('1d0')
    maximum = dice.max()
    assert maximum == 0, 'Dice("1d0").max() != 0, Dice("1d0").max() == %s' % maximum
    print('Dice("1d0").max() == 0, OK')

    dice = Dice('1d0')
    minimum = dice.min()
    assert minimum == 0, 'Dice("1d0").min() != 0, Dice("1d0").min() == %s' % minimum
    print('Dice("1d0").min() == 0, OK')

    dice = Dice('0d1')
    maximum = dice.max()
    assert maximum == 0, 'Dice("0d1").max() != 0, Dice("0d1").max() == %s' % maximum
    print('Dice("0d1").max() == 0, OK')

    dice = Dice('0d1')
    minimum = dice.min()
    assert minimum == 0, 'Dice("0d1").min() != 0, Dice("0d1").min() == %s' % minimum
    print('Dice("0d1").min() == 0, OK')

    for count in range(1, 51):
        for base in range(1, 51):
            dice_str = get_dice_str(count, base)
            dice = Dice(dice_str)
            roll_range = range(1, count * base + 1)
            for i in range(100):
                roll = dice.roll()
                assert roll in roll_range, 'Dice("{dice_str}").roll() out of range({minimum}, {maximum}), Dice("{dice_str}").roll() == {roll}'.format(dice_str=dice_str, roll=roll, minimum=roll_range[0], maximum=roll_range[-1])
    print('Dice("<count>d<base>").roll() with count and base parameters in range 1-50 is valid, OK')

    dice = Dice()
    for i in range(100):
        roll = dice.roll()
        assert roll == 0, 'Dice().roll() != 0, Dice"0d0").roll() == %s' % roll
    print('Dice().roll() == 0, OK')

    dice = Dice('0d0')
    for i in range(100):
        roll = dice.roll()
        assert roll == 0, 'Dice("0d0").roll() != 0, Dice("0d0").roll() == %s' % roll
    print('Dice("0d0").roll() == 0, OK')

    dice = Dice('1d0')
    for i in range(100):
        roll = dice.roll()
        assert roll == 0, 'Dice("1d0").roll() != 0, Dice("1d0").roll() == %s' % roll
    print('Dice("1d0").roll() == 0, OK')

    dice = Dice('0d1')
    for i in range(100):
        roll = dice.roll()
        assert roll == 0, 'Dice("0d1").roll() != 0, Dice("0d1").roll() == %s' % roll
    print('Dice("0d1").roll() == 0, OK')

    print("---"*20)
    print("Dice test finished")
    print("---"*20)

    # GurpsDice test

    print("---"*20)
    print("GurpsDice test start")
    print("---"*20)

    g_dice = GurpsDice()
    assert g_dice.__str__() == '1d6', 'GurpsDice() != "1d6", GurpsDice() == %s' % g_dice
    print('GurpsDice() == "1d6", OK')

    g_dice = GurpsDice('1d6')
    assert g_dice.__str__() == '1d6', 'GurpsDice("1d6") != "1d6", GurpsDice("1d6") == %s' % g_dice
    print('GurpsDice("1d6") == "1d6", OK')

    g_dice = GurpsDice('159d6')
    assert g_dice.__str__() == '159d6', 'GurpsDice("159d6") != "1d6", GurpsDice("159d6") == %s' % g_dice
    print('GurpsDice("159d6") == "159d6", OK')

    print("---"*20)
    print("GurpsDice test finished")
    print("---"*20)
