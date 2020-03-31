"""
给定一个二叉树和其中一个节点，如何找出中旭便利序列的下一个节点？
树中的节点除了有两个分别指向左，右自节点的指针，还有一个指向父节点的指针。
"""
import doctest
import Trees


def q8(node):
    """
    >>> q8(tree.root.left) # b的下一个节点是h
    h
    >>> q8(tree.root.left.left) # d的下一个节点是b
    b
    >>> q8(tree.root.left.right.right) # i的下一个节点是a
    a
    """
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        print(node.value)
        return
    elif node.parent.left is node:
        print(node.parent.value)
        return
    else:
        while node.parent is not None:
            if node.parent.left is node:
                print(node.parent.value)
                return
            else:
                node = node.parent
                continue
        print(node.value)
        return


if __name__ == '__main__':
    tree = Trees.BTree(with_parent=True)
    tree.build(pre_ord=['a', 'b', 'd', 'e', 'h', 'i', 'c', 'f', 'g'],
               in_ord=['d', 'b', 'h', 'e', 'i', 'a', 'f', 'c', 'g'])
    if not doctest.testmod().failed:
        print('Well Done!')
