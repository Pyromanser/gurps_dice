import random
from gurps_dice import Dice, GurpsDice, EmptyDiceError, DiceFaceError, DiceCountError, DiceBonusError
from gurps_dice_handful import HandfulDice

run_test_dice = True
run_test_gurps_dice = True


def random_int(start, end, excluding=()):
    r_int = random.randint(start, end)
    if r_int in excluding:
        r_int = random_int(start, end, excluding)
    return r_int


def get_dice_str(count, face, bonus=0):
    dice_str = "{:d}d{:d}".format(count, face)
    if bonus:
        dice_str += "{:+d}".format(bonus)
    return dice_str


def test(result_of_test, error_message, format_values):
    if result_of_test:
        print("OK")
    else:
        print("Fail")
        assert result_of_test, error_message.format(**format_values)


def test_error():
    pass


def test_dice():
    print("---"*20)
    print("Dice test start")
    print("---"*20)

    print('Dice() == "0d0", ', end='')
    dice = Dice()
    test(dice.__str__() == '0d0', 'Dice() != "0d0", Dice() == {dice}', {'dice': dice})

    print('Dice("<count>d<face>") with count and face parameters in range 0-100 is valid, ', end='')
    for count in range(101):
        for face in range(101):
            dice_str = get_dice_str(count, face)
            dice = Dice(dice_str)
            test(dice.__str__() == dice_str, 'Dice("{dice_str}") != "{dice_str}", Dice("{dice_str}") == {dice}', {'dice_str':dice_str, 'dice':dice})

    for count in range(101):
        for face in range(101):
            for bonus in (x for x in range(-101, 101) if x != 0):
                dice_str = get_dice_str(count, face, bonus)
                try:
                    dice = Dice(dice_str)
                except EmptyDiceError:
                    pass
                else:
                    assert False, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<face>±<bonus>") with count, face and "bonus" parameters in range 0-100 raise EmptyDiceError, OK')

    for count in range(101):
        for face in range(101):
            for bonus_str in ("+0", "-0"):
                dice_str = get_dice_str(count, face) + bonus_str
                try:
                    dice = Dice(dice_str)
                except EmptyDiceError:
                    pass
                else:
                    assert False, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<face>±0") with count and face in range 0-100 and "bonus" equal 0 parameters raise EmptyDiceError, OK')

    for count in range(-100, 0):
        for face in range(101):
            dice_str = get_dice_str(count, face)
            try:
                dice = Dice(dice_str)
            except EmptyDiceError:
                pass
            else:
                assert False, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<face>") with count in range -100-0 and face in range 0-100 parameters in range 0-100 raise EmptyDiceError, OK')

    for count in range(101):
        for face in range(-100, 0):
            dice_str = get_dice_str(count, face)
            try:
                dice = Dice(dice_str)
            except EmptyDiceError:
                pass
            else:
                assert False, 'Dice("{dice_str}") should raise EmptyDiceError, Dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('Dice("<count>d<face>") with count in range 0-100 and face in range -100-0 parameters in range 0-100 raise EmptyDiceError, OK')

    for face in range(101):
        for count in range(101):
            dice_str = get_dice_str(count, face)
            dice = Dice(count, face)
            assert dice.__str__() == dice_str, 'Dice({count}, {face}) != "{dice_str}", Dice({count}, {face}) == {dice}'.format(dice_str=dice_str, count=count, face=face, dice=dice)
    print('Dice(count, face) with count and face parameters in range 0-100 is valid, OK')

    for face in range(101):
        for count1 in range(101):
            for count2 in range(101):
                dice_str = get_dice_str(count1 + count2, face)
                dice1 = Dice(count1, face)
                dice2 = Dice(count2, face)
                dice = (dice1 + dice2)
                assert dice.__str__() == dice_str, 'Dice({count1}, {face}) + Dice({count2}, {face}) != "{dice_str}", Dice({count1}, {face}) + Dice({count2}, {face}) == {dice}'.format(dice_str=dice_str, count1=count1, count2=count2, face=face, dice=dice)
    print('Dice(count1, face) + Dice(count2, face) with counts and face parameters in range 0-100 is valid, OK')

    for count1 in range(51):
        for count2 in range(51):
            for face1 in range(51):
                for face2 in range(51):
                    if face1 == face2:
                        continue
                    dice1 = Dice(count1, face1)
                    dice2 = Dice(count2, face2)
                    try:
                        dice = (dice1 + dice2)
                    except DiceFaceError:
                        pass
                    else:
                        assert False, 'Dice({count1}, {face1}) + Dice({count2}, {face2}) should raise DiceFaceError, Dice({count1}, {face1}) + Dice({count2}, {face2}) == {dice}'.format(count1=count1, count2=count2, face1=face1, face2=face2, dice=dice)
    print('Dice(count1, face1) + Dice(count2, face2) with count1 and count2 in range 0-50, face1 and face2 in disjoint range 0-50 raise DiceFaceError, OK')

    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 + dice2)
    except TypeError:
        print('Dice(1, 20) + "1d20" raise TypeError, OK')
    else:
        assert False, 'Dice(1, 20) + "1d20" should raise TypeError, Dice(1, 20) + "1d20" == %s' % dice

    dice1 = Dice(1, 20)
    bonus = 1
    try:
        dice = (dice1 + bonus)
    except TypeError:
        print('Dice(1, 20) + 1 raise TypeError, OK')
    else:
        assert False, 'Dice(1, 20) + 1 should raise TypeError, Dice(1, 20) + 1 == %s' % dice

    for face in range(101):
        for count1 in range(101):
            for count2 in range(101):
                if count2 > count1:
                    continue
                dice_str = get_dice_str(count1 - count2, face)
                dice1 = Dice(count1, face)
                dice2 = Dice(count2, face)
                dice = (dice1 - dice2)
                assert dice.__str__() == dice_str, 'Dice({count1}, {face}) - Dice({count2}, {face}) != "{dice_str}", Dice({count1}, {face}) - Dice({count2}, {face}) == {dice}'.format(dice_str=dice_str, count1=count1, count2=count2, face=face, dice=dice)
    print('Dice(count1, face) - Dice(count2, face) with count1 and count2 on condition count2 > count1 and face parameters in range 0-100 is valid, OK')

    for face in range(101):
        for count1 in range(101):
            for count2 in range(101):
                if count2 <= count1:
                    continue
                dice1 = Dice(count1, face)
                dice2 = Dice(count2, face)
                try:
                    dice = (dice1 - dice2)
                except DiceCountError:
                    pass
                else:
                    assert False, 'Dice({count1}, {face}) - Dice({count2}, {face}) should raise DiceCountError, Dice({count1}, {face}) - Dice({count2}, {face}) == {dice}'.format(count1=count1, count2=count2, face=face, dice=dice)
    print('Dice(count1, face) - Dice(count2, face) with count1 and count2 on condition count2 <= count1 and face parameters in range 0-100 raise DiceCountError, OK')

    for count1 in range(51):
        for count2 in range(51):
            for face1 in range(51):
                for face2 in range(51):
                    if face1 == face2 or count1 > count2:
                        continue
                    dice1 = Dice(count1, face1)
                    dice2 = Dice(count2, face2)
                    try:
                        dice = (dice1 - dice2)
                    except DiceFaceError:
                        pass
                    else:
                        assert False, 'Dice({count1}, {face1}) - Dice({count2}, {face2}) should raise DiceFaceError, Dice({count1}, {face1}) - Dice({count2}, {face2}) == {dice}'.format(count1=count1, count2=count2, face1=face1, face2=face2, dice=dice)
    print('Dice(count1, face1) - Dice(count2, face2) with count1 and count2 in range 0-50, face1 on condition count2 > count1 and face2 in disjoint range 0-50 raise DiceFaceError, OK')

    dice1 = Dice(1, 20)
    dice2 = "1d20"
    try:
        dice = (dice1 - dice2)
    except TypeError:
        print('Dice(1, 20) - "1d20" raise TypeError, OK')
    else:
        assert False, 'Dice(1, 20) - "1d20" should raise TypeError, Dice(1, 20) - "1d20" == %s' % dice

    dice1 = Dice(1, 20)
    bonus = 1
    try:
        dice = (dice1 - bonus)
    except TypeError:
        print('Dice(1, 20) - 1 raise TypeError, OK')
    else:
        assert False, 'Dice(1, 20) - 1 should raise TypeError, Dice(1, 20) - 1 == %s' % dice

    for count in range(101):
        for face in range(101):
            dice_str = get_dice_str(count, face)
            dice = Dice()
            dice.set_dice(dice_str)
            assert dice.__str__() == dice_str, 'dice.set_dice("{dice_str}") != "{dice_str}", dice.set_dice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('dice.set_dice("<count>d<face>") with count and face parameters in range 0-100 is valid, OK')

    for count in range(101):
        for face in range(101):
            dice_str = get_dice_str(count, face)
            dice = Dice()
            dice.set_dice(count, face)
            assert dice.__str__() == dice_str, 'dice.set_dice({count}, {face}) != "{dice_str}", dice.set_dice({count}, {face}) == {dice}'.format(dice_str=dice_str, count=count, face=face, dice=dice)
    print('dice.set_dice(count, face) with count and face parameters in range 0-100 is valid, OK')

    for face in range(101):
        dice_str = get_dice_str(0, face)
        dice = Dice()
        dice.set_face(face)
        assert dice.__str__() == dice_str, 'dice.set_face({face}) != "{dice_str}", dice.set_face({face}) == {dice}'.format(dice_str=dice_str, face=face, dice=dice)
    print('dice.set_face(face) with face parameter in range 0-100 is valid, OK')

    for count in range(101):
        dice_str = get_dice_str(count, 0)
        dice = Dice()
        dice.set_count(count)
        assert dice.__str__() == dice_str, 'dice.set_count({count}) != "{dice_str}", dice.set_count({count}) == {dice}'.format(dice_str=dice_str, count=count, dice=dice)
    print('dice.set_count(count) with count parameter in range 0-100 is valid, OK')

    for count in range(1, 101):
        for face in range(1, 101):
            dice_str = get_dice_str(count, face)
            maximum_assert = count * face
            dice = Dice(dice_str)
            maximum = dice.max()
            assert maximum == maximum_assert, 'Dice("{dice_str}").max() != {maximum_assert}, Dice("{dice_str}").max() == {maximum}'.format(dice_str=dice_str, maximum_assert=maximum_assert, maximum=maximum)
    print('Dice("<count>d<face>").max() with count and face parameters in range 1-100 is valid, OK')

    for count in range(1, 101):
        for face in range(1, 101):
            dice_str = get_dice_str(count, face)
            minimum_assert = count
            dice = Dice(dice_str)
            minimum = dice.min()
            assert minimum == minimum_assert, 'Dice("{dice_str}").min() != {minimum_assert}, Dice("{dice_str}").min() == {minimum}'.format(dice_str=dice_str, minimum_assert=minimum_assert, minimum=minimum)
    print('Dice("<count>d<face>").min() with count and face parameters in range 1-100 is valid, OK')

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
        for face in range(1, 51):
            dice_str = get_dice_str(count, face)
            dice = Dice(dice_str)
            roll_range = range(1, count * face + 1)
            for i in range(100):
                roll = dice.roll()
                assert roll in roll_range, 'Dice("{dice_str}").roll() out of range({minimum}, {maximum}), Dice("{dice_str}").roll() == {roll}'.format(dice_str=dice_str, roll=roll, minimum=roll_range[0], maximum=roll_range[-1])
    print('Dice("<count>d<face>").roll() with count and face parameters in range 1-50 is valid, OK')

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


def test_gurps_dice():
    print("---"*20)
    print("GurpsDice test start")
    print("---"*20)

    dice = GurpsDice()
    assert dice.__str__() == '1d6', 'GurpsDice() != "1d6", GurpsDice() == %s' % dice
    print('GurpsDice() == "1d6", OK')

    for count in range(101):
        dice_str = get_dice_str(count, 6)
        dice = GurpsDice(dice_str)
        assert dice.__str__() == dice_str, 'GurpsDice("{dice_str}") != "{dice_str}", GurpsDice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('GurpsDice("<count>d6") with count parameter in range 0-100 is valid, OK')

    for count in range(101):
        for bonus_str in ('+0', '-0'):
            dice_str = get_dice_str(count, 6)
            dice_input_str = dice_str + bonus_str
            dice = GurpsDice(dice_input_str)
            assert dice.__str__() == dice_str, 'GurpsDice("{dice_input_str}") != "{dice_str}", GurpsDice("{dice_input_str}") == {dice}'.format(dice_str=dice_str, dice_input_str=dice_input_str, dice=dice)
    print('GurpsDice("<count>d6±0") with count parameter in range 0-100 is valid, OK')

    for count in range(101):
        for bonus in range(-101, 101):
            dice_str = get_dice_str(count, 6, bonus)
            dice = GurpsDice(dice_str)
            assert dice.__str__() == dice_str, 'GurpsDice("{dice_str}") != "{dice_str}", GurpsDice("{dice_str}") == {dice}'.format(dice_str=dice_str, dice=dice)
    print('GurpsDice("<count>d6±<bonus>") with count in range 0-100 and bonus in range -100-100 parameters is valid, OK')

    print("---"*20)
    print("GurpsDice test finished")
    print("---"*20)

if run_test_dice:
    test_dice()
if run_test_gurps_dice:
    test_gurps_dice()
