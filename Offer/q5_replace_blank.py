"""
把字符串中的每个空格替换成"%20"。
例如输入"We are happy.", 则输出"We%20are%20happy."
"""
import doctest


def q5(string):
    """
    >>> q5("We are happy.")
    We%20are%20happy.
    """
    print(string.replace(' ', '%20'))
    return None


if __name__ == '__main__':
    if not doctest.testmod().failed:
        print(f'Well Done!')
