"""
在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。
输入一个这样的二维数组和一个整数，判断是否含有该整数。
"""
import doctest


def q4(matrix, num):
    """
    >>> q4([[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]], 5)
    False
    >>> q4([[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]], 7)
    True
    >>> q4([[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]], 15)
    True
    >>> q4([[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]], 1)
    True
    >>> q4([[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]], 'a')
    Input Error!
    """
    i, j = 0, len(matrix[0]) - 1
    try:
        while i < len(matrix) and j > -1:
            if matrix[i][j] == num:
                return True
            elif matrix[i][j] > num:
                j -= 1
                continue
            elif matrix[i][j] < num:
                i += 1
                continue
    except TypeError:
        print(f'Input Error!')
        return None
    return False


if __name__ == '__main__':
    if not doctest.testmod().failed:
        print(f'Well Done!')
