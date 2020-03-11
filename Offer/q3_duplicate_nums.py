"""
面试题3：数组中重复的数字
在一个长度为n的数组里的所有数字都在0～n-1范围内。数组中某些数字是重复的，
但不知道有个数字重复了，也不知道每个数字冲了了几次。
请找出数组中任意一个重复的数字。
例如输入长度为7的数组[2,3,1,0,2,5,3]，那么对应的输出是重复的数字2或者3。
"""
import doctest


def q3_1(lis):
    """
    >>> q3_1([2,3,1,0,2,5,3])
    2
    >>> q3_1([])
    Empty List!
    >>> q3_1([2, 2, 2, 2, 2])
    2
    >>> q3_1([3, 2, 3])
    Length Error!
    >>> q3_1(['a'])
    Invalid Input!
    >>> q3_1([0, 1, 2, 3])
    no duplicate nums
    """
    if not len(lis):
        print(f'Empty List!')
        return None
    hash_list = [-1] * len(lis)
    for i in lis:
        try:
            if hash_list[i] == -1:
                hash_list[i] = i
            else:
                return i
        except IndexError:
            print(f'Length Error!')
            return None
        except TypeError:
            print(f'Invalid Input!')
            return None
    print(f'no duplicate nums')
    return None


def q3_2(lis):
    """
    >>> q3_2([2,3,5,4,3,2,6,7])
    2
    >>> q3_2([])
    Empty List!
    >>> q3_2([2, 2, 2, 2, 2])
    2
    >>> q3_2([3, 2, 3])
    Length Error!
    >>> q3_2(['a'])
    Invalid Input!
    >>> q3_2([0, 1, 2, 3])
    no duplicate nums
    """
    if not len(lis):
        print(f'Empty List!')
        return None
    try:
        for i in range(len(lis)):
            while lis[i] != i:
                if lis[i] == lis[lis[i]]:
                    return lis[i]
                x = lis[i]
                y = lis[x]
                lis[i] = y
                lis[x] = x
                i = lis.index(y)
        print(f'no duplicate nums')
        return None
    except IndexError:
        print(f'Length Error!')
        return None
    except TypeError:
        print(f'Invalid Input!')
        return None


if __name__ == '__main__':
    if not doctest.testmod().failed:
        print(f'Well Done!')
