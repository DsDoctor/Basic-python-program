def print_progress(cur, tol, _l=20):
    """
    小工具打印进度
    cur 现在进行了多少
    tol 一共有多少
    _l 进度条长度默认20
    使用：
        if __name__ == '__main__':
            lis = range(777)
            for i in lis:
                print_progress(i, len(lis))
                time.sleep(0.01)
            print_progress(1, 1)
            print('next')
    """
    print(f"\r|{''*(int((cur/tol)*_l))}{' '*(_l-int((cur/tol)*_l))}|{cur/tol*100:.4f}%", end='\n'if cur == tol else'')


def get_lcs(s1, s2):
    """
    获取两个字符串的最长公共子序列
    :param s1: 字符串1
    :param s2: 字符串2
    :return: 返回最长公共子序列长度
    """
    matrix = [[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if s1[i-1] == s2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]+1
            else:
                matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1])
    return matrix[-1][-1]


def run_time(f):
    """
    定义装饰器
    若定义函数时 用@run_time装饰 则可输出函数运行时间
    """
    import time

    def inner():
        start = time.time()
        f()
        end = time.time()
        print(f'function {str(f.__name__)} run in {end-start:.2f} sec')
    return inner


if __name__ == '__main__':
    print(get_lcs('是不是玩不起了', '卧槽还玩不玩了'))
