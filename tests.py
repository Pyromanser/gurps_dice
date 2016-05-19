import time
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

    # time.sleep(0.05)
    dice = Dice()
    assert dice.__str__() == '0d0', 'Dice() != "0d0", Dice() == %s' % dice
    print('Dice() == "0d0", OK')

    # time.sleep(0.05)
    dice = Dice('1d6')
    assert dice.__str__() == '1d6', 'Dice("1d6") != "1d6", Dice("1d6") == %s' % dice
    print('Dice("1d6") == "1d6", OK')

    # time.sleep(0.05)
    for i in range(100):
        dice_str = get_dice_str(random_int(10, 1000), random_int(10, 1000))
        dice = Dice(dice_str)
        assert dice.__str__() == dice_str, 'Dice("{dice_str}") != "{dice_str}", Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with random count and base parameters is valid, OK')

    # time.sleep(0.05)
    for i in range(100):
        dice_str = get_dice_str(random_int(0, 1000), random_int(0, 1000), random_int(-100, 100, (0,)))
        try:
            dice = Dice(dice_str)
        except EmptyDiceError:
            pass
        else:
            assert True, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<base>") with random count, base and "bonus" parameters raise EmptyDiceError, OK')

    # time.sleep(0.05)
    try:
        dice = Dice('-1d6')
    except EmptyDiceError:
        print('Dice("-1d6") raise EmptyDiceError, OK')
    else:
        assert True, 'Dice("-1d6") should raise EmptyDiceError, Dice("-1d6") == %s' % dice

    # time.sleep(0.05)
    try:
        dice = Dice('1d-6')
    except EmptyDiceError:
        print('Dice("1d-6") raise EmptyDiceError, OK')
    else:
        assert True, 'Dice("1d-6") should raise EmptyDiceError, Dice("1d-6") == %s' % dice

    # time.sleep(0.05)
    for i in range(100):
        count, base = random_int(0, 1000), random_int(0, 1000)
        dice_str = get_dice_str(count, base)
        dice = Dice(count, base)
        assert dice.__str__() == dice_str, 'Dice({count}, {base}) != "{dice_str}", Dice({count}, {base}) == {dice}'.format(dice_str=dice_str, count=count, base=base, dice=dice)
    print('Dice(count, base) with random count and base parameters is valid, OK')

    # time.sleep(0.05)
    for i in range(100):
        base = random_int(0, 1000)
        count1, count2 = random_int(0, 1000), random_int(0, 1000)
        dice1_str = get_dice_str(count1, base)
        dice2_str = get_dice_str(count2, base)
        dice_str = get_dice_str(count1 + count2, base)
        dice1 = Dice(count1, base)
        dice2 = Dice(count2, base)
        dice = (dice1 + dice2)
        assert dice.__str__() == dice_str, 'Dice({count1}, {base}) + Dice({count2}, {base}) != "{dice_str}", Dice({count1}, {base}) + Dice({count2}, {base}) == {dice}'.format(dice_str=dice_str, count1=count1, count2=count2, base=base, dice=dice)
    print('Dice(count1, base) + Dice(count2, base) with random counts and base parameters is valid, OK')

    # time.sleep(0.05)
    dice1 = Dice(1, 20)
    dice2 = Dice(2, 6)
    try:
        dice = (dice1 + dice2)
    except BaseDiceError:
        print('Dice(1, 20) + Dice(2, 6) raise BaseDiceError, OK')
    else:
        assert True, 'Dice(1, 20) + Dice(2, 6) should raise BaseDiceError, Dice(1, 20) + Dice(2, 6) == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 + dice2)
    except TypeError:
        print('Dice(1, 20) + "1d20" raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) + "1d20" should raise TypeError, Dice(1, 20) + "1d20" == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(1, 20)
    dice2 = 1
    try:
        dice = (dice1 + dice2)
    except TypeError:
        print('Dice(1, 20) + 1 raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) + 1 should raise TypeError, Dice(1, 20) + 1 == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(3, 20)
    dice2 = Dice(2, 20)
    dice = (dice1 - dice2)
    assert dice.__str__() == '1d20', 'Dice(3, 20) - Dice(2, 20) != "1d20", Dice(3, 20) - Dice(2, 20) == %s' % dice
    print('Dice(3, 20) - Dice(2, 20) == "1d20", OK')

    # time.sleep(0.05)
    dice1 = Dice(2, 20)
    dice2 = Dice(3, 20)
    try:
        dice = (dice1 - dice2)
    except CountDiceError:
        print('Dice(2, 20) - Dice(3, 20) raise CountDiceError, OK')
    else:
        assert True, 'Dice(2, 20) - Dice(3, 20) should raise CountDiceError, Dice(2, 20) - Dice(3, 20) == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(3, 20)
    dice2 = Dice(2, 6)
    try:
        dice = (dice1 - dice2)
    except BaseDiceError:
        print('Dice(3, 20) - Dice(2, 6) raise BaseDiceError, OK')
    else:
        assert True, 'Dice(3, 20) - Dice(2, 6) should raise BaseDiceError, Dice(3, 20) - Dice(2, 6) == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 - dice2)
    except TypeError:
        print('Dice(1, 20) - "1d20" raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) - "1d20" should raise TypeError, Dice(1, 20) - "1d20" == %s' % dice

    # time.sleep(0.05)
    dice1 = Dice(1, 20)
    dice2 = 1
    try:
        dice = (dice1 - dice2)
    except TypeError:
        print('Dice(1, 20) - 1 raise TypeError, OK')
    else:
        assert True, 'Dice(1, 20) - 1 should raise TypeError, Dice(1, 20) - 1 == %s' % dice

    # time.sleep(0.05)
    dice = Dice()
    dice.set_dice('1d6')
    assert dice.__str__() == '1d6', 'dice.set_dice("1d6") != "1d6", dice.set_dice("1d6") == %s' % dice
    print('dice.set_dice("1d6") == "1d6", OK')

    # time.sleep(0.05)
    dice = Dice()
    dice.set_dice(1, 6)
    assert dice.__str__() == '1d6', 'dice.set_dice(1, 6) != "1d6", dice.set_dice(1, 6) == %s' % dice
    print('dice.set_dice(1, 6) == "1d6", OK')

    # time.sleep(0.05)
    dice = Dice()
    dice.set_base(1)
    assert dice.__str__() == '0d1', 'dice.set_base(1) != "0d1", dice.set_base(1) == %s' % dice
    print('dice.set_base(1) == "0d1", OK')

    # time.sleep(0.05)
    dice = Dice()
    dice.set_count(1)
    assert dice.__str__() == '1d0', 'dice.set_count(1) != "1d0", dice.set_count(1) == %s' % dice
    print('dice.set_count(1) == "1d0", OK')

    # time.sleep(0.05)
    dice = Dice('1d6')
    maximum = dice.max()
    assert maximum == 6, 'Dice("1d6").max() != 6, Dice("1d6").max() == %s' % maximum
    print('Dice("1d6").max() == 6, OK')

    # time.sleep(0.05)
    dice = Dice('1d6')
    minimum = dice.min()
    assert minimum == 1, 'Dice("1d6").min() != 1, Dice("1d6").min() == %s' % minimum
    print('Dice("1d6").min() == 1, OK')

    # time.sleep(0.05)
    dice = Dice()
    maximum = dice.max()
    assert maximum == 0, 'Dice().max() != 0, Dice().max() == %s' % maximum
    print('Dice().max() == 0, OK')

    # time.sleep(0.05)
    dice = Dice()
    minimum = dice.min()
    assert minimum == 0, 'Dice().min() != 0, Dice().min() == %s' % minimum
    print('Dice().min() == 0, OK')

    # time.sleep(0.05)
    dice = Dice('1d0')
    maximum = dice.max()
    assert maximum == 0, 'Dice("1d0").max() != 0, Dice("1d0").max() == %s' % maximum
    print('Dice("1d0").max() == 0, OK')

    # time.sleep(0.05)
    dice = Dice('1d0')
    minimum = dice.min()
    assert minimum == 0, 'Dice("1d0").min() != 0, Dice("1d0").min() == %s' % minimum
    print('Dice("1d0").min() == 0, OK')

    # time.sleep(0.05)
    dice = Dice('0d1')
    maximum = dice.max()
    assert maximum == 0, 'Dice("0d1").max() != 0, Dice("0d1").max() == %s' % maximum
    print('Dice("0d1").max() == 0, OK')

    # time.sleep(0.05)
    dice = Dice('0d1')
    minimum = dice.min()
    assert minimum == 0, 'Dice("0d1").min() != 0, Dice("0d1").min() == %s' % minimum
    print('Dice("0d1").min() == 0, OK')

    # time.sleep(0.05)
    dice = Dice('1d6')
    roll = dice.roll()
    for i in range(100):
        assert 0 < roll <= 6, 'Dice("1d6").roll() out of range, Dice("1d6").roll() == %s' % roll
    print('Dice("1d6").roll() <= 6 and Dice("1d6").roll() > 0, OK')

    # time.sleep(0.05)
    dice = Dice('2d6')
    roll = dice.roll()
    for i in range(100):
        assert 0 < roll <= 6*2, 'Dice("2d6").roll() out of range, Dice("2d6").roll() == %s' % roll
    print('Dice("2d6").roll() <= 12 and Dice("2d6").roll() > 0, OK')

    # time.sleep(0.05)
    dice = Dice('3d20')
    roll = dice.roll()
    for i in range(100):
        assert 0 < roll <= 20*3, 'Dice("3d20").roll() out of range, Dice("3d20").roll() == %s' % roll
    print('Dice("3d20").roll() <= 60 and Dice("3d20").roll() > 0, OK')

    print("---"*20)
    print("Dice test finished")
    print("---"*20)

    # GurpsDice test

    print("---"*20)
    print("GurpsDice test start")
    print("---"*20)

    # time.sleep(0.05)
    g_dice = GurpsDice()
    assert g_dice.__str__() == '1d6', 'GurpsDice() != "1d6", GurpsDice() == %s' % g_dice
    print('GurpsDice() == "1d6", OK')

    # time.sleep(0.05)
    g_dice = GurpsDice('1d6')
    assert g_dice.__str__() == '1d6', 'GurpsDice("1d6") != "1d6", GurpsDice("1d6") == %s' % g_dice
    print('GurpsDice("1d6") == "1d6", OK')

    # time.sleep(0.05)
    g_dice = GurpsDice('159d6')
    assert g_dice.__str__() == '159d6', 'GurpsDice("159d6") != "1d6", GurpsDice("159d6") == %s' % g_dice
    print('GurpsDice("159d6") == "159d6", OK')

    print("---"*20)
    print("GurpsDice test finished")
    print("---"*20)
