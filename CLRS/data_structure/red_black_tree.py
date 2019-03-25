class TreeNode:
    def __init__(self, val=None, color=None, left=None, right=None, parent=None):
        self.val = val
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self, root):
        self.root = root

    def left_rotate(self, node):
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.left.parent:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right