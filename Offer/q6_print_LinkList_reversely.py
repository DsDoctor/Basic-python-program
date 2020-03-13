"""
输入一个链表的头节点，从尾到头打印每个节点的值
"""
import doctest


class Node:
    def __init__(self, num):
        self.value = num
        self.next = None


class LinkList:
    def __init__(self, lis):
        if not len(lis):
            self.start = None
        else:
            self.start = node = Node(lis[0])
            for i in range(1, len(lis)):
                node.next = Node(lis[i])
                node = node.next


def q_1(node):
    """
    >>> lis = [1,2,3,4]; node = LinkList(lis).start; q_1(node)
    4
    3
    2
    1
    """
    if node.next is not None:
        q_1(node.next)
    print(node.value)
    return None


def q_2(node):
    """
    >>> lis = [1,2,3,4]; node = LinkList(lis).start; q_2(node)
    4,3,2,1
    """
    stack = []
    while node is not None:
        stack.append(node.value)
        node = node.next
    res = ''
    while len(stack):
        num = stack.pop(-1)
        res = res + str(num) + ','
    print(res[:-1])
    return None


if __name__ == '__main__':
    if not doctest.testmod().failed:
        print('Well Done!')
