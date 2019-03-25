import random


class TreeNode:
    def __init__(self, val=None, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTree:
    def __init__(self, root):
        self.root = root

    def in_order_tree_walk(self, root):
        if not root:
            return
        self.in_order_tree_walk(root.left)
        print(root.val)
        self.in_order_tree_walk(root.right)

    def tree_search(self, root, val):
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.tree_search(root.left, val)
        else:
            return self.tree_search(root.right, val)

    def iterative_tree_search(self, root, val):
        while root and val != root.val:
            if val < root.val:
                root = root.left
            else:
                root = root.right
        return root

    def tree_minimum(self, root):
        while root.left:
            root = root.left
        return root

    def tree_maximum(self, root):
        while root.right:
            root = root.right
        return root

    def tree_successor(self, root):
        if root.right:
            return self.tree_minimum(root.right)
        parent = root.parent
        while parent and root == parent.right:
            root = parent
            parent = parent.parent
        return parent

    def tree_insert(self, node):
        cur = self.root
        parent = None
        while cur:
            parent = cur
            if node.val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        node.parent = parent
        if not parent:
            self.root = node
        elif node.val < parent.val:
            parent.left = node
        else:
            parent.right = node

    def transplant(self, node1, node2):
        if not node1.parent:
            self.root = node2
        elif node1 is node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.left = node2
        if node2:
            node2.parent = node1.parent

    def tree_delete(self, node):
        if not node.left:
            self.transplant(node, node.right)
        elif not node.right:
            self.transplant(node, node.left)
        else:
            parent = self.tree_minimum(node.right)
            if parent.parent != node:
                self.transplant(parent, parent.right)
                parent.right = node.right
                parent.right.parent = parent
            self.transplant(node, parent)
            parent.left = node.left
            parent.left.parent = parent


if __name__ == '__main__':
    tree = BinarySearchTree(None)
    for i in range(10):
        tree.tree_insert(TreeNode(random.randint(0, 1000)))
    tree.in_order_tree_walk(tree.root)
    print('二叉搜索树最小值')
    print(tree.tree_minimum(tree.root).val)
    print('二叉搜索树最大值')
    print(tree.tree_maximum(tree.root).val)
    print('二叉搜索树后继')
    print(tree.root.val)
    print(tree.tree_successor(tree.root).val)