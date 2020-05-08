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


def print_progress(cur, tol, _l=20):
    print(f"\r|{''*(int((cur/tol)*_l))}{' '*(_l-int((cur/tol)*_l))}|{cur/tol*100:.2f}%", end='\n'if cur == tol else'')
