class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class BTree:
    def __init__(self, with_parent=False):
        self.root = None
        self.size = 0
        self.with_parent = with_parent

    def build(self, pre_ord=None, in_ord=None, pos_ord=None):
        if pre_ord and in_ord and not pos_ord:
            self.root = self.__build_pre_in(pre_ord, in_ord)
        elif in_ord and pos_ord and not pre_ord:
            self.root = self.__build_in_pos(in_ord, pos_ord)
        else:
            return None
        return self

    def __build_pre_in(self, pre_ord, in_ord):
        if not len(pre_ord):
            return None
        if len(in_ord) == 1:
            self.size += 1
            return TreeNode(pre_ord[0])
        root = TreeNode(pre_ord[0])
        self.size += 1
        index = in_ord.index(pre_ord[0])
        root.left = self.__build_pre_in(pre_ord[1:index+1], in_ord[:index])
        if root.left is not None and self.with_parent:
            root.left.parent = root
        root.right = self.__build_pre_in(pre_ord[index+1:], in_ord[index+1:])
        if root.right is not None and self.with_parent:
            root.right.parent = root
        return root

    def __build_in_pos(self, in_ord, pos_ord):
        if not len(pos_ord):
            return None
        if len(pos_ord) == 1:
            self.size += 1
            return TreeNode(pos_ord[-1])
        root = TreeNode(pos_ord[-1])
        self.size += 1
        index = in_ord.index(pos_ord[-1])
        root.left = self.__build_in_pos(in_ord[:index], pos_ord[:index])
        if root.left is not None and self.with_parent:
            root.left.parent = root
        root.right = self.__build_in_pos(in_ord[index+1:], pos_ord[index:-1])
        if root.right is not None and self.with_parent:
            root.right.parent = root
        return root


if __name__ == '__main__':
    btree_1 = BTree()
    btree_1.build(pre_ord=[1, 2, 4, 7, 3, 5, 6, 8], in_ord=[4, 7, 2, 1, 5, 3, 8, 6])
    btree_2 = BTree(with_parent=True)
    btree_2.build(in_ord=[4, 7, 2, 1, 5, 3, 8, 6], pos_ord=[7, 4, 2, 5, 8, 6, 3, 1])
    pass
