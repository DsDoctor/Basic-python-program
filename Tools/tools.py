"""
小工具打印进度
使用：
    if __name__ == '__main__':
        lis = range(777)
        for i in lis:
            print_progress(i, len(lis))
            time.sleep(0.01)
        print_progress(1, 1)
        print('next')
"""


def print_progress(cur, tol):
    print(f"\r|{''*(int((cur/tol)*20))}{' '*(20-int((cur/tol)*20))}| {cur/tol*100:.2f}%", end='')
    if cur == tol:
        print()
