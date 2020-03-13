"""
输入某二叉树的前序遍历和中序遍历结果，重建二叉树。               1
假设输入的前序遍历和中序遍历结果中都不含重复的数字。          2      3
例如输入前序遍历序列[1,2,4,7,3,5,6,8]               4       5    6
输入的中序遍历序列[4,7,2,1,5,3,8,6]                   7        8
重建二叉树并返回头节点
"""
import doctest


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def q(pre_order, in_order):
    """
    >>> q([1,2,4,7,3,5,6,8],[4,7,2,1,5,3,8,6])
    1
    """
    if not len(pre_order):
        return None
    if len(pre_order) == 1:
        return TreeNode(pre_order[0])
    index = in_order.index(pre_order[0])
    root = TreeNode(pre_order[0])
    root.left = q(pre_order[1:index+1], in_order[:index])
    root.right = q(pre_order[index+1:], in_order[index+1:])
    return root


if __name__ == '__main__':
    if not doctest.testmod().failed:
        print('Well Done!')
